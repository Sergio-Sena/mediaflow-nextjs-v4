# -*- coding: utf-8 -*-
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

local_path = r'C:\Users\dell 5557\Videos\IDM'

original_folders = [
    '404_Hot_Found', 'Aidra_Fox', 'Alice_sexy', 'Allinika', 'anastangel',
    'angel', 'angelica', 'Angelica_Heaven', 'AniButler', 'Anime',
    'AquaRi', 'Ariana_fox', 'arina_fox', 'Asian', 'Atlanta_Moreno',
    'blacked', 'Camgirls', 'Candy_Love', 'Carla_cutie', 'charmig',
    'Cicil_dool', 'Coco_love', 'Comatozze', 'Creamy_Spot', 'Crystal_angells',
    'CumForKate', 'Cumpilation', 'DD_Porn_adventure', 'Diana_Rider',
    'DickForLily', 'Dillion', 'Dollbabybell', 'Dolly_Rud', 'Ellie_moore',
    'Elly_Clutch', 'Emilia_Shot', 'Emillya_Bunny', 'Estie_Kay', 'Face_to_cam',
    'Honey_Sasha', 'Hot_Pearl', 'I_m_Gona_n_cum', 'Jenny_Kitty',
    'Jill Kassidy', 'julie_jesse', 'Kate_Kuray', 'Kera_Bear_s', 'KittyxKun',
    'Kristal_Jack', 'Kukupaiii', 'Lana', 'Leah_Meow', 'Lil_Karina',
    'LinaMigurtt', 'Lisinha', 'LIs_Evans', 'litle_dragon', 'Little_Angel',
    'Little_Caprice', 'MariMoore', 'MayaLis', 'megan', 'MiaMalkova',
    'MickLiter', 'Mini_skirt_dress', 'MIRARI_HUB', 'Miuzxc', 'noMercy',
    'parasite', 'PMV', 'Puffy_Pink', 'ReisLin', 'Riley_Reid', 'Rose_Rider',
    'Secret_Elle', 'ShyBlanche', 'Sienna_Sky', 'skye_young', 'solazola',
    'sonia_vibe', 'Spirite_Moon', 'Squir7een', 'Star', 'SweetFox', 'TUSHY',
    'Update_Wife', 'Vallery_Ray', 'Verlonis_s', 'Yuiwoo', 'Zoe_Neli'
]

created = 0
existed = 0
for folder in original_folders:
    folder_path = os.path.join(local_path, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        created += 1
    else:
        existed += 1

print(f'Pastas recriadas: {created}')
print(f'Ja existiam: {existed}')
print(f'Total: {created + existed}')
