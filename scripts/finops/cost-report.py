#!/usr/bin/env python3
"""
MidiaFlow FinOps - Cost Report + AI Insights
Collects AWS costs, analyzes with Bedrock Claude, sends report via SES.
"""
import boto3
import json
import os
from datetime import datetime, timedelta, timezone

REGION = os.environ.get('AWS_REGION', 'us-east-1')
EMAIL_TO = os.environ.get('FINOPS_EMAIL', 'senanetworker@gmail.com')
EMAIL_FROM = EMAIL_TO
COMMIT_SHA = os.environ.get('GITHUB_SHA', 'local')[:8]
PROJECT = 'MidiaFlow'

ce = boto3.client('ce', region_name=REGION)
bedrock = boto3.client('bedrock-runtime', region_name=REGION)
ses = boto3.client('ses', region_name=REGION)


TAG_FILTER = {'Tags': {'Key': 'Project', 'Values': ['MidiaFlow'], 'MatchOptions': ['EQUALS']}}


def get_costs():
    """Get costs per service for last 30 days filtered by Project=MidiaFlow."""
    end = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    start = (datetime.now(timezone.utc) - timedelta(days=30)).strftime('%Y-%m-%d')

    try:
        resp = ce.get_cost_and_usage(
            TimePeriod={'Start': start, 'End': end},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}],
            Filter=TAG_FILTER
        )
    except Exception as e:
        print(f"Cost Explorer error (tag filter may take 24h to activate): {e}")
        return [], 0.0

    services = []
    total = 0.0
    for period in resp.get('ResultsByTime', []):
        for group in period.get('Groups', []):
            name = group['Keys'][0]
            cost = float(group['Metrics']['UnblendedCost']['Amount'])
            if cost > 0.001:
                services.append({'name': name, 'cost': cost})
                total += cost

    services.sort(key=lambda x: x['cost'], reverse=True)
    return services, round(total, 2)


def get_previous_month_costs():
    """Get previous month total for comparison filtered by Project=MidiaFlow."""
    end = (datetime.now(timezone.utc).replace(day=1)).strftime('%Y-%m-%d')
    start = (datetime.now(timezone.utc).replace(day=1) - timedelta(days=30)).strftime('%Y-%m-%d')

    try:
        resp = ce.get_cost_and_usage(
            TimePeriod={'Start': start, 'End': end},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            Filter=TAG_FILTER
        )
        for period in resp.get('ResultsByTime', []):
            return float(period['Metrics']['UnblendedCost']['Amount'])
    except:
        return 0.0


def get_ai_insights(services, total, prev_total):
    """Get optimization insights from Bedrock Claude."""
    cost_data = "\n".join([f"- {s['name']}: ${s['cost']:.2f}" for s in services[:10]])

    prompt = f"""Você é um consultor FinOps AWS. Analise os custos do projeto {PROJECT} e dê 3 sugestões práticas de otimização em português.

Custos últimos 30 dias (total: ${total:.2f}):
{cost_data}

Mês anterior: ${prev_total:.2f}
Variação: {((total - prev_total) / prev_total * 100) if prev_total > 0 else 0:.1f}%

Infraestrutura: S3 (storage + hosting), CloudFront (CDN), Lambda (17 funções Python), DynamoDB (users/logs), API Gateway (REST).

Responda APENAS com 3 insights curtos e acionáveis. Formato:
1. [insight]
2. [insight]
3. [insight]"""

    try:
        resp = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                'anthropic_version': 'bedrock-2023-05-31',
                'max_tokens': 300,
                'messages': [{'role': 'user', 'content': prompt}]
            })
        )
        result = json.loads(resp['body'].read())
        return result['content'][0]['text']
    except Exception as e:
        print(f"Bedrock error: {e}")
        return "Insights indisponíveis no momento."


def build_html(services, total, prev_total, insights):
    """Build HTML email report."""
    variation = ((total - prev_total) / prev_total * 100) if prev_total > 0 else 0
    var_color = '#e74c3c' if variation > 0 else '#2ecc71'
    var_icon = '📈' if variation > 0 else '📉'
    now = datetime.now(timezone.utc).strftime('%d/%m/%Y %H:%M UTC')

    rows = ""
    for s in services[:10]:
        pct = (s['cost'] / total * 100) if total > 0 else 0
        bar_width = min(pct, 100)
        rows += f"""
        <tr>
          <td style="padding:8px 12px;border-bottom:1px solid #2a2a3e;color:#e0e0e0">{s['name']}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #2a2a3e;color:#00ffff;text-align:right;font-weight:bold">${s['cost']:.2f}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #2a2a3e;width:120px">
            <div style="background:#1a1a2e;border-radius:4px;overflow:hidden;height:8px">
              <div style="background:linear-gradient(90deg,#00ffff,#7b2ff7);width:{bar_width}%;height:100%"></div>
            </div>
          </td>
        </tr>"""

    insights_html = insights.replace('\n', '<br>')

    return f"""
    <div style="background:#0d0d1a;padding:20px;font-family:Arial,sans-serif;max-width:650px;margin:0 auto">
      <div style="background:linear-gradient(135deg,#1a1a2e,#16213e);border:1px solid #00ffff33;border-radius:12px;overflow:hidden">
        
        <div style="background:linear-gradient(90deg,#00ffff22,#7b2ff722);padding:20px 24px;border-bottom:1px solid #00ffff33">
          <h1 style="margin:0;color:#00ffff;font-size:22px">📊 {PROJECT} - Relatório FinOps</h1>
          <p style="margin:4px 0 0;color:#888;font-size:13px">Deploy: {COMMIT_SHA} | {now}</p>
        </div>

        <div style="padding:20px 24px">
          <div style="display:flex;gap:12px;margin-bottom:20px">
            <div style="flex:1;background:#0d0d1a;border:1px solid #00ffff33;border-radius:8px;padding:16px;text-align:center">
              <p style="margin:0;color:#888;font-size:12px">CUSTO (30 DIAS)</p>
              <p style="margin:4px 0 0;color:#00ffff;font-size:28px;font-weight:bold">${total:.2f}</p>
            </div>
            <div style="flex:1;background:#0d0d1a;border:1px solid #00ffff33;border-radius:8px;padding:16px;text-align:center">
              <p style="margin:0;color:#888;font-size:12px">MÊS ANTERIOR</p>
              <p style="margin:4px 0 0;color:#e0e0e0;font-size:28px;font-weight:bold">${prev_total:.2f}</p>
            </div>
            <div style="flex:1;background:#0d0d1a;border:1px solid #00ffff33;border-radius:8px;padding:16px;text-align:center">
              <p style="margin:0;color:#888;font-size:12px">VARIAÇÃO</p>
              <p style="margin:4px 0 0;color:{var_color};font-size:28px;font-weight:bold">{var_icon} {variation:+.1f}%</p>
            </div>
          </div>

          <h2 style="color:#e0e0e0;font-size:16px;margin:20px 0 10px;border-bottom:1px solid #2a2a3e;padding-bottom:8px">💰 Custos por Serviço</h2>
          <table style="width:100%;border-collapse:collapse">
            <tr>
              <th style="padding:8px 12px;text-align:left;color:#888;font-size:12px;border-bottom:2px solid #00ffff33">SERVIÇO</th>
              <th style="padding:8px 12px;text-align:right;color:#888;font-size:12px;border-bottom:2px solid #00ffff33">CUSTO</th>
              <th style="padding:8px 12px;color:#888;font-size:12px;border-bottom:2px solid #00ffff33">%</th>
            </tr>
            {rows}
          </table>

          <div style="margin-top:20px;background:#0d0d1a;border:1px solid #7b2ff755;border-radius:8px;padding:16px">
            <h2 style="color:#7b2ff7;font-size:16px;margin:0 0 10px">🤖 AI Insights (Claude)</h2>
            <p style="color:#e0e0e0;font-size:14px;line-height:1.6;margin:0">{insights_html}</p>
          </div>

          <p style="color:#555;font-size:11px;text-align:center;margin-top:20px">
            Gerado automaticamente por MidiaFlow FinOps | Powered by AWS Bedrock
          </p>
        </div>
      </div>
    </div>"""


def send_email(html):
    """Send report via SES."""
    try:
        ses.send_email(
            Source=EMAIL_FROM,
            Destination={'ToAddresses': [EMAIL_TO]},
            Message={
                'Subject': {
                    'Data': f'📊 {PROJECT} FinOps - Deploy {COMMIT_SHA} | ${0:.2f}',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Html': {'Data': html, 'Charset': 'UTF-8'}
                }
            }
        )
        print(f"✅ Report sent to {EMAIL_TO}")
    except Exception as e:
        print(f"❌ SES error: {e}")


def main():
    print(f"📊 {PROJECT} FinOps Report")
    print("=" * 40)

    print("1. Collecting costs...")
    services, total = get_costs()

    print("2. Getting previous month...")
    prev_total = get_previous_month_costs()

    print(f"   Current: ${total:.2f} | Previous: ${prev_total:.2f}")

    print("3. Getting AI insights...")
    insights = get_ai_insights(services, total, prev_total)
    print(f"   {insights[:80]}...")

    print("4. Building report...")
    html = build_html(services, total, prev_total, insights)

    # Fix subject with actual total
    global send_email
    _send = send_email

    def send_email_fixed(h):
        ses.send_email(
            Source=EMAIL_FROM,
            Destination={'ToAddresses': [EMAIL_TO]},
            Message={
                'Subject': {
                    'Data': f'📊 {PROJECT} FinOps - Deploy {COMMIT_SHA} | ${total:.2f}',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Html': {'Data': h, 'Charset': 'UTF-8'}
                }
            }
        )
        print(f"✅ Report sent to {EMAIL_TO}")

    print("5. Sending email...")
    send_email_fixed(html)

    print("=" * 40)
    print(f"✅ Done! Total: ${total:.2f}")


if __name__ == '__main__':
    main()
