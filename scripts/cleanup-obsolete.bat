@echo off
echo ========================================
echo  LIMPEZA DE SCRIPTS OBSOLETOS
echo ========================================
echo.

REM Scripts de upload obsoletos (manter apenas os genericos)
move scripts\upload-kate-kuray-simple.py _archive\scripts-old\
move scripts\upload-kate-kuray-star.py _archive\scripts-old\
move scripts\upload-kate-kuray-missing-only.py _archive\scripts-old\
move scripts\upload-star-complete.py _archive\scripts-old\
move scripts\upload-star-final.py _archive\scripts-old\
move scripts\upload-star-progress.py _archive\scripts-old\
move scripts\upload-star-local.py _archive\scripts-old\
move scripts\upload-star-sanitized.py _archive\scripts-old\
move scripts\upload-star-sergio.py _archive\scripts-old\
move scripts\upload-star-idm.py _archive\scripts-old\
move scripts\upload-comatozze.py _archive\scripts-old\
move scripts\upload-comatozze-progress.py _archive\scripts-old\
move scripts\upload-comatozze-real.py _archive\scripts-old\
move scripts\upload-shyblanche.py _archive\scripts-old\
move scripts\upload-tushy.py _archive\scripts-old\
move scripts\upload-katekuray.py _archive\scripts-old\
move scripts\upload-mia-malkova.py _archive\scripts-old\
move scripts\upload-sweetfox-progress.py _archive\scripts-old\
move scripts\upload-anasta-sanitized.py _archive\scripts-old\
move scripts\upload-missing-anasta.py _archive\scripts-old\
move scripts\upload-missing-kate-kuray.py _archive\scripts-old\
move scripts\upload-missing-mirari.py _archive\scripts-old\
move scripts\upload-moana-lidlima.py _archive\scripts-old\
move scripts\upload-lid-lima-pastas.py _archive\scripts-old\
move scripts\upload-limpar-lid-lima.py _archive\scripts-old\
move scripts\upload-carros-lid-lima.py _archive\scripts-old\
move scripts\upload-carros-progress.py _archive\scripts-old\
move scripts\upload-carros-um-por-vez.py _archive\scripts-old\
move scripts\upload-seletivo-sergio-sena.py _archive\scripts-old\
move scripts\upload-ts-to-s3.py _archive\scripts-old\
move scripts\upload-1-comatozze.py _archive\scripts-old\
move scripts\upload-2-shyblanche.py _archive\scripts-old\
move scripts\upload-3-tushy.py _archive\scripts-old\
move scripts\upload-4-katekuray.py _archive\scripts-old\

REM Scripts de check obsoletos
move scripts\check-sergio-files.py _archive\scripts-old\
move scripts\check-sergio-sena.py _archive\scripts-old\
move scripts\check-sergio-structure.py _archive\scripts-old\
move scripts\check-sergio-structure-simple.py _archive\scripts-old\
move scripts\check-all-admin-files.py _archive\scripts-old\
move scripts\check-admin-vs-sergio.py _archive\scripts-old\
move scripts\check-anasta-upload.py _archive\scripts-old\
move scripts\check-comatozze-local.py _archive\scripts-old\
move scripts\check-lid-lima-files.py _archive\scripts-old\
move scripts\check-lid-lima.py _archive\scripts-old\
move scripts\check-lilo-stitch.py _archive\scripts-old\
move scripts\check-star-folder-issue.py _archive\scripts-old\
move scripts\check-star-upload.py _archive\scripts-old\
move scripts\check-video-folders.py _archive\scripts-old\

REM Scripts de rename/move obsoletos
move scripts\rename-remove-tilde.py _archive\scripts-old\
move scripts\move-all-sergio-videos.py _archive\scripts-old\
move scripts\move-anime-folders.py _archive\scripts-old\
move scripts\move-anime-to-admin.py _archive\scripts-old\
move scripts\move-eporner-file.py _archive\scripts-old\
move scripts\move-katekura.py _archive\scripts-old\
move scripts\move-sergio-videos-final.py _archive\scripts-old\
move scripts\move-sergio-videos-to-root.py _archive\scripts-old\
move scripts\move-ts-only.py _archive\scripts-old\

REM Scripts de verificacao obsoletos
move scripts\verificar-conversao-ts.py _archive\scripts-old\
move scripts\verificar-kate-kuray-s3.py _archive\scripts-old\
move scripts\verificar-star-sergio.py _archive\scripts-old\
move scripts\verificar-star-vs-faltantes.py _archive\scripts-old\
move scripts\verificar-todas-pastas-s3.py _archive\scripts-old\
move scripts\verificar-videos-lid-lima-simples.py _archive\scripts-old\
move scripts\verificar-videos-lid-lima.py _archive\scripts-old\

REM Scripts de compare obsoletos
move scripts\comparar-local-sergio-sena.py _archive\scripts-old\
move scripts\comparar-local-sergio-simples.py _archive\scripts-old\
move scripts\compare-kate-kuray-simple.py _archive\scripts-old\
move scripts\compare-kate-kuray.py _archive\scripts-old\
move scripts\compare-mia-malkova.py _archive\scripts-old\

REM Scripts de unify/organize obsoletos
move scripts\unificar-lid-lima.py _archive\scripts-old\
move scripts\unify-404-folders.py _archive\scripts-old\
move scripts\unify-kate-kuray.py _archive\scripts-old\
move scripts\unify-litle-dragon.py _archive\scripts-old\
move scripts\organizar-anime-completo.js _archive\scripts-old\
move scripts\organizar-anime-sem-copia.js _archive\scripts-old\

REM Scripts de find/list obsoletos
move scripts\find-carros-video.py _archive\scripts-old\
move scripts\find-lilo-stitch-videos.py _archive\scripts-old\
move scripts\find-missing-files.py _archive\scripts-old\
move scripts\list-404-folders.py _archive\scripts-old\
move scripts\list-star-subfolders.py _archive\scripts-old\
move scripts\list-user-admin-folders.py _archive\scripts-old\

REM Scripts de convert obsoletos
move scripts\converter-carros-real.py _archive\scripts-old\
move scripts\converter-mkv-carros-lilo.py _archive\scripts-old\
move scripts\convert-and-upload-ts.py _archive\scripts-old\

REM Scripts de delete/cleanup obsoletos
move scripts\delete-and-upload-comatozze.py _archive\scripts-old\
move scripts\delete-anonymous-folder.py _archive\scripts-old\
move scripts\delete-duplicates-admin.py _archive\scripts-old\
move scripts\delete-empty-users-folder.py _archive\scripts-old\
move scripts\delete-folder-placeholder.py _archive\scripts-old\
move scripts\delete-old-cloudfront.py _archive\scripts-old\
move scripts\deletar-arquivos-ts.py _archive\scripts-old\
move scripts\cleanup-multipart-uploads.py _archive\scripts-old\
move scripts\cleanup-s3-anonymous.py _archive\scripts-old\

REM Scripts de fix obsoletos
move scripts\fix-comatozze-local.py _archive\scripts-old\
move scripts\fix-duplicated-paths.py _archive\scripts-old\
move scripts\fix-s3-prefix.py _archive\scripts-old\
move scripts\fix-user-role-permissions.py _archive\scripts-old\

REM Scripts de replace obsoletos
move scripts\replace-kate-kuray.py _archive\scripts-old\
move scripts\replace-moana-mp4.py _archive\scripts-old\
move scripts\substituir-videos-idm.py _archive\scripts-old\

REM Scripts de scan/duplicates obsoletos
move scripts\scan-all-duplicates.py _archive\scripts-old\
move scripts\scan-duplicates-advanced.py _archive\scripts-old\
move scripts\find-duplicates-admin.py _archive\scripts-old\
move scripts\execute-duplicates-cleanup.py _archive\scripts-old\

REM Scripts de migrate obsoletos
move scripts\migrate-admin-to-sergio.py _archive\scripts-old\
move scripts\migrate-cloudfront-complete.py _archive\scripts-old\
move scripts\migrate-cloudfront.py _archive\scripts-old\
move scripts\rollback-migration.py _archive\scripts-old\

REM Scripts de test obsoletos
move scripts\test-lambda-final.py _archive\scripts-old\
move scripts\test-lid-lima-auth.py _archive\scripts-old\
move scripts\test-lid-login.py _archive\scripts-old\
move scripts\test-viewer-login.py _archive\scripts-old\
move scripts\test-view-api-auto.py _archive\scripts-old\
move scripts\test-view-api.py _archive\scripts-old\

REM Scripts JS obsoletos
move scripts\buscar-jiggly-profundo.js _archive\scripts-old\
move scripts\buscar-jiggly.js _archive\scripts-old\
move scripts\buscar-mover-imagem.js _archive\scripts-old\
move scripts\buscar-todas-imagens-anime.js _archive\scripts-old\
move scripts\buscar-todos-jiggly-s3.js _archive\scripts-old\
move scripts\contar-arquivos.js _archive\scripts-old\
move scripts\contar-imagem.js _archive\scripts-old\
move scripts\contar-jiggly-s3.js _archive\scripts-old\
move scripts\deletar-truncados-nsfw.js _archive\scripts-old\
move scripts\divide-pasta.js _archive\scripts-old\
move scripts\dividir-recursivo.js _archive\scripts-old\
move scripts\enviar-faltantes-nsfw.js _archive\scripts-old\
move scripts\identificar-faltantes-jiggly.js _archive\scripts-old\
move scripts\listar-fotos-admin.js _archive\scripts-old\
move scripts\listar-jiggly-completo.js _archive\scripts-old\
move scripts\upload-anime-pastas.js _archive\scripts-old\
move scripts\upload-jiggly-local.js _archive\scripts-old\
move scripts\upload-jiggly.js _archive\scripts-old\
move scripts\verificar-duplicados-anime.js _archive\scripts-old\
move scripts\verificar-nsfw-duplicados.js _archive\scripts-old\
move scripts\verificar-pics-notebackup.js _archive\scripts-old\

REM Scripts BAT obsoletos
move scripts\upload-kate-one-by-one.bat _archive\scripts-old\
move scripts\upload-re4-7gb.bat _archive\scripts-old\
move scripts\upload-star-cli.bat _archive\scripts-old\
move scripts\upload-star-folder.bat _archive\scripts-old\

REM Outros obsoletos
move scripts\duplicados_admin.txt _archive\scripts-old\
move scripts\duplicados_avancado.json _archive\scripts-old\
move scripts\duplicados_avancado.txt _archive\scripts-old\
move scripts\duplicados_completo.json _archive\scripts-old\
move scripts\duplicados_completo.txt _archive\scripts-old\
move scripts\s3-structure-report.md _archive\scripts-old\
move scripts\session-summary-v4.6.md _archive\scripts-old\

echo.
echo ========================================
echo  LIMPEZA CONCLUIDA
echo ========================================
echo.
echo Scripts obsoletos movidos para: _archive\scripts-old\
echo.
