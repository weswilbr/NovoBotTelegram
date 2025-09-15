# NOME DO ARQUIVO: features/products/data.py
# REFACTOR: Centraliza todos os file_ids de mídias e textos com uma estrutura padronizada e completa.

"""
Este arquivo é a "fonte da verdade" para todas as mídias e textos do bot.
Manter tudo centralizado aqui torna a atualização de file_ids e a adição
de novos produtos uma tarefa simples, sem a necessidade de alterar a lógica
nos arquivos de handlers.
"""

MEDIA = {
    # --- Mídias Gerais (não são produtos do menu) ---
    'bonusconstrutormidias': {
        'video1': 'BAACAgEAAxkBAAJAU2fGAtnueBNRnb1LCqFFFfHG35OYAAJcBQACS1kxRuel2nL4TjefNgQ',
        'documento': 'BAACAgEAAxkBAAJAVWfGBGDBfHcAAXBT7LRKfZTnTKNG7QACYAUAAktZMUbZVJlfL5F_9jYE'
    },
    'fatorestransf': {
        'video1': {'type': 'video', 'id': 'BAACAgEAAxkBAAJJMGfqtNj0QxKXG4FOpQS95NmJXcupAAJKBgAC-9pZR5ORbjj6QwSVNgQ'},
        'video2': {'type': 'video', 'id': 'BAACAgEAAxkBAAJB8WfOAhRPVUK8u9LxuB-BSIXDPfTKAALSBAACynwwRMxkekB46LmzNgQ'},
        'table': {'type': 'document', 'id': 'BQACAgEAAxkBAAIw6Gc4xcpWr6KivsAiGUwOpwcID0wxAALjBAAChl_IRdQoqw0PYFCgNgQ'},
    },
    'fabrica4life': {
        'armazem': 'BAACAgEAAxkBAAIBMGbncmJda7Sz-CPPc4unHFYjinjdAAK6CwACz0RBR_6nHEgo0YTmNgQ',
        'envase': 'BAACAgEAAxkBAAIBMmbndcrrkMOWppQGRixAh_CbE4oeAAK7CwACz0RBRypfMI6d_CjQNgQ',
    },
    'folheteria': {
        'panfletoprodutosnovo': 'BQACAgEAAxkBAAIhW2cdTj5i9HqUKjzciT-waYnZUIj0AAIOBQACw_vpRCemtnyqP0xmNgQ',
    },
    'catalogoprodutos': {
        'documento': 'BQACAgEAAxkBAAIxj2c45EdaH76knO_Xm1drcy3S4uqGAAL0BAAChl_IRZzzUO7vIgo4NgQ'
    },
    'recompensas2024': {
        'documento': 'BQACAgEAAxkBAANJZuXs2N0B' 'GNgYFLeOGs0btJjgYkEAAvED' 'AAKYvDBHHRLaoQgyoHU2BA'
    },
    'planotrabalho90dias': {
        'pdf': 'BQACAgEAAxkBAANXZuXtZG2ZHLUjyXFzvmpc32A0m28AAvQDAAKYvDBHeMndEw69BD02BA',
        'ppt': 'BAACAgEAAxkBAAIDa2bpX_0PhR7Iq9vZNaUmfRLxv4pjAALJBAACNzRIR5jQpmV2G0XjNgQ'
    },
    'marketing_rede': {
        "video": "BAACAgEAAxkBAAIxpmc46CYHNY8qufZwAXQXw7z7eAspAAL2BAAChl_IRf-DsXQNjmvONgQ"
    },
    
    # --- DICIONÁRIO PRINCIPAL DE PRODUTOS PARA O MENU DINÂMICO ---
    'produtos': {
        'riovidaburst': {
            'label': "🫐 RioVida Burst",
            'foto': 'AgACAgEAAxkBAAJIw2fpaw-kaCGnsMvkQ7_-n_5e1KNQAAJArTEbGpNJR71s3kcAAXAnIgEAAwIAA3kAAzYE',
            'video': 'BAACAgEAAxkBAAJUX2iXLsqb7Xov4heg8nOpkgAB7jXg8wAC-wUAAp6JuUSAbsjdTnY92zYE',
            'documento': 'BQACAgEAAxkBAAMxZt4kyxybDpyStV695_x9BqHi-gUAAp0DAAJbOfFGNpvdNZiPoXc2BA',
            'social_kit': {
                'story_image': 'PLACEHOLDER_STORY_IMAGE_RIOVIDABURST',
                'feed_image': 'PLACEHOLDER_FEED_IMAGE_RIOVIDABURST',
                'reels_video': 'PLACEHOLDER_REELS_VIDEO_RIOVIDABURST',
                'copy_text': "🍇 Energia e imunidade em um só lugar! 🍇\n\nCom o RioVida Burst, você tem o poder dos antioxidantes e dos Fatores de Transferência na palma da sua mão. Perfeito para a correria do dia a dia!\n\n✅ Fortalece o sistema imunológico\n✅ Aumenta a energia e a disposição\n✅ Sabor delicioso de açaí e blueberry\n\nQuer sentir essa explosão de bem-estar? Fale comigo e peça já o seu! 🚀",
                'hashtags': "#4LifeBrasil #RioVidaBurst #FatoresDeTransferencia #Saude #ImunidadeEmAlta #Antioxidantes #VidaSaudavel"
            }
        },
        'riovidastix': {
            'label': "🍷 RioVida Stix",
            'foto': 'AgACAgEAAxkBAAJPbmgzNgToTi1BSLHEfjSkJUbkp8z1AAJarjEbp3-YRS-ZYpO590cxAQADAgADeQADNgQ',
            'video': 'BAACAgEAAxkBAAJBSmfGPZK4y6Yq5XNuodprmReqbhWjAAJzBQACS1kxRoWhJ5c0q9C0NgQ',
            'documento': 'BQACAgEAAx0CfAGLsgACCPRm9B5_NQTLMkliTyY38WGKPbzWPgACfwQAAqQtoUdHteDxrzz-jDYE',
            'social_kit': {
                'story_image': 'PLACEHOLDER_STORY_IMAGE_RIOVIDASTIX',
                'feed_image': 'PLACEHOLDER_FEED_IMAGE_RIOVIDASTIX',
                'reels_video': 'PLACEHOLDER_REELS_VIDEO_RIOVIDASTIX',
                'copy_text': "💦 Transforme sua água, transforme sua saúde! 💦\n\nRioVida Stix é a forma mais prática e deliciosa de fortalecer sua imunidade e se manter hidratado ao longo do dia. Basta misturar na água e pronto!\n\n✅ Suporte ao sistema imunológico\n✅ Rico em antioxidantes\n✅ Prático para levar a qualquer lugar\n\nPronto para dar um upgrade na sua hidratação? Fale comigo! ✨",
                'hashtags': "#RioVidaStix #4Life #Hidratacao #Imunidade #BemEstar #Antioxidante #SaudeEmPo"
            }
        },
        'bioefa': {
            'label': "🌿 BioEFA",
            'foto': 'AgACAgEAAxkBAAJIuGfpaff9kWF09Y3UfOSPx5iTLN4PAAI1rTEbGpNJRxv12_knzg0BAQADAgADeQADNgQ',
            'video': 'BAACAgEAAxkBAAJPSmgyl2euQMx0brhHHHxgN9sVWb8IAAL_BAACp3-QRd8S7iFF1DKQNgQ',
            'documento': 'BQACAgEAAxkBAAJDmWfY5EKUqzRUd93IGl95fZiZCK8jAAIwBAAC55rIRot5b1n-bCGKNgQ',
            'social_kit': {
                'story_image': 'PLACEHOLDER_STORY_IMAGE_BIOEFA',
                'feed_image': 'PLACEHOLDER_FEED_IMAGE_BIOEFA',
                'reels_video': 'PLACEHOLDER_REELS_VIDEO_BIOEFA',
                'copy_text': "🧠❤️ Cuide do seu corpo de dentro para fora com BioEFA! 🌿\n\nEssenciais para o coração, cérebro e bem-estar geral, os ácidos graxos ômega-3 e ômega-6 são a base para uma vida saudável. BioEFA combina óleos de peixe e sementes da mais alta qualidade.\n\n✅ Suporte à saúde cardiovascular\n✅ Promove a função cerebral saudável\n✅ Ajuda a manter a pele radiante\n\nInvista no seu bem-estar completo. Vamos conversar! 💬",
                'hashtags': "#BioEFA #Omega3 #SaudeDoCoracao #4LifeBrasil #Nutricao #PeleSaudavel #CerebroAtivo"
            }
        },
        'energygostix': {
            'label': "⚡ Energy Go Stix",
            'foto': 'AgACAgEAAxkBAAJIy2fpbA57ndR7vG0J_MehK_shs20EAAJHrTEbGpNJR6TVL1LEoIJqAQADAgADeQADNgQ',
            'video': 'BAACAgEAAxkBAAJUYWiXL7D1KBC-hKBm9WqMRKAyXc9XAAL-BQACnom5RBgycWAwtSjYNgQ',
            'documento': 'BQACAgEAAxkBAAMzZt4lSZsZzqZyVGKuz9eUKr7Vq2EAAp4DAAJbOfFG8zorKuHMfh82BA',
            'social_kit': {
                'story_image': 'PLACEHOLDER_STORY_IMAGE_ENERGY',
                'feed_image': 'PLACEHOLDER_FEED_IMAGE_ENERGY',
                'reels_video': 'PLACEHOLDER_REELS_VIDEO_ENERGY',
                'copy_text': "⚡ Dê um basta no cansaço e acenda sua energia com Energy Go Stix! ⚡\n\nPrecisa de um impulso para o trabalho, estudos ou treino? Energy Go Stix combina Fatores de Transferência com ingredientes naturais para dar foco e vitalidade ao seu dia.\n\n✅ Aumenta a energia e o desempenho\n✅ Melhora o foco e a concentração\n✅ Delicioso sabor de frutas vermelhas\n\nTransforme seu dia! Me chame para saber como. 🔥",
                'hashtags': "#EnergyGoStix #MaisEnergia #FocoTotal #4Life #SemCansaco #Performance #VidaAtiva"
            }
        },
        'tfplus': {
            'label': "🛡️ TF Plus",
            'foto': 'AgACAgEAAxkBAAJIz2fpbIe8Z0ura7cnY-o12mJ7nKy3AAJIrTEbGpNJR2I6ds8Po1kTAQADAgADeQADNgQ',
            'video': 'BAACAgEAAxkBAAICtmboFTTgNOCnGllv5Ff-5-914JOHAAIGCgACz0RJR8say1htm3VaNgQ',
            'documento': 'BQACAgEAAxkBAAICu2boFqVza6DHajduav8Bt9BewjnkAAIICgACz0RJR4CWyGtgxbNuNgQ',
            'social_kit': {
                'story_image': 'AgACAgEAAxkBAAIB1WjGL1pYKU9CqvRwedxhW6v-n_aWAAKAtzEbwFI4RmspPKiDU1qtAQADAgADeQADNgQ',
                'feed_image': 'PLACEHOLDER_FEED_IMAGE_TFPLUS',
                'reels_video': 'PLACEHOLDER_REELS_VIDEO_TFPLUS',
                'copy_text': "🛡️ Blinde sua imunidade com a fórmula mais avançada: TF Plus! 🛡️\n\nConsiderado o topo de linha do suporte ao sistema imunológico, o TF Plus combina a inteligência dos Fatores de Transferência com um blend exclusivo de ingredientes para uma defesa robusta.\n\n✅ O mais alto nível de suporte imunológico\n✅ Educa e equilibra as células de defesa\n✅ Promove saúde e bem-estar geral\n\nProteja quem você ama. Fale comigo e fortaleça sua saúde! 💪",
                'hashtags': "#TFPlus #Imunidade #SistemaImunologico #4Life #FatoresDeTransferencia #SaudeBlindada #BemEstar"
            }
        },
        'tfplus30caps': {
            'label': "💊 TF Plus (30 Cápsulas)",
            'foto': 'AgACAgEAAyEFAASNSVRUAAIE5mgybu_TgvyRS614CG0vhPSEbw11AAIHrjEbtX-RRT-pYabHSFYlAQADAgADeQADNgQ',
            'video': 'BAACAgEAAxkBAAIB0mjGLgoWgELYYwzo6ojAQHNRJSaKAALhBQACwFI4Rkl4PHUfOWYAATYE',
            'documento': None,
            'social_kit': {
                'story_image': 'PLACEHOLDER_STORY_IMAGE_TFPLUS30',
                'feed_image': 'PLACEHOLDER_FEED_IMAGE_TFPLUS30',
                'reels_video': 'PLACEHOLDER_REELS_VIDEO_TFPLUS30',
                'copy_text': "💊 Praticidade e potência para sua imunidade! 💊\n\nA fórmula completa do TF Plus, agora em uma embalagem compacta de 30 cápsulas. Perfeita para viagens ou para quem quer experimentar o poder do nosso suporte imunológico mais vendido.\n\n✅ Mesma fórmula, mais conveniência\n✅ Ideal para levar na bolsa ou na mala\n✅ Suporte imunológico de elite onde você estiver\n\nLeve sua proteção com você. Peça já a versão de 30 cápsulas! ✈️",
                'hashtags': "#TFPlus30 #Praticidade #ImunidadeParaViagem #4LifeBrasil #Suplementos"
            }
        },
        'tfzinco': {
            'label': "💪 TF Zinco",
            'foto': 'AgACAgEAAxkBAAJI02fpbK-_ZDexRnc3YzDeKDGms_mQAAJJrTEbGpNJR1EGLzdAaKE2AQADAgADeQADNgQ',
            'video': 'BAACAgEAAxkBAAI7qWeaTq2zU48iBsEtLdJOOCNL2f8QAAKZBwACL8jQRM8VaZzyHN22NgQ',
            'documento': 'BQACAgEAAxkBAAJD-WfaIbM6LYt8sjD-YhouWGpOsZrrAAL-AwACtxWgR04AAdqdDwaCXTYE',
            'social_kit': {
                'story_image': 'PLACEHOLDER_STORY_IMAGE_TFZINCO',
                'feed_image': 'PLACEHOLDER_FEED_IMAGE_TFZINCO',
                'reels_video': 'PLACEHOLDER_REELS_VIDEO_TFZINCO',
                'copy_text': "💪 A dupla perfeita para sua imunidade: Fator de Transferência + Zinco! 💪\n\nTF Zinco combina a inteligência do Tri-Factor Formula com o poder do zinco, um mineral essencial para o funcionamento das células de defesa. Cuidado diário de forma prática e eficaz.\n\n✅ Suporte essencial ao sistema imunológico\n✅ Ação antioxidante\n✅ Ajuda na saúde da pele\n\nUm pequeno passo para uma grande proteção. Peça o seu! 🛡️",
                'hashtags': "#TFZinco #Zinco #ImunidadeForte #4LifeBrasil #SaudeDiaria #Protecao"
            }
        },
        'nutrastart': {
            'label': "🥤 NutraStart",
            'foto': 'AgACAgEAAxkBAAJI12fpbOCMcR3xZwx-ENLIWWmg-pYKAAJKrTEbGpNJR2HM_u4rWwytAQADAgADeQADNgQ',
            'video': 'BAACAgEAAxkBAAIDg2bpZaLV-92rwmxh78pNb9BPXTLPAALKBAACNzRIRwqUwDWOqKb8NgQ',
            'documento': 'BQACAgEAAxkBAAIDhWbpZ0BRUjZluUdXfzEZ0L4hV-vyAALLBAACNzRIR22E4cGkGvHoNgQ',
            'social_kit': {
                'story_image': 'PLACEHOLDER_STORY_IMAGE_NUTRASTART',
                'feed_image': 'PLACEHOLDER_FEED_IMAGE_NUTRASTART',
                'reels_video': 'PLACEHOLDER_REELS_VIDEO_NUTRASTART',
                'copy_text': "☀️ Comece seu dia da melhor forma com NutraStart! ☀️\n\nUma refeição completa, deliciosa e nutritiva em um copo. NutraStart é um shake que oferece proteínas, fibras, vitaminas e o suporte imunológico dos Fatores de Transferência. Perfeito para um café da manhã saudável ou para o controle de peso.\n\n✅ Nutrição balanceada\n✅ Apoio ao sistema imunológico\n✅ Sabor incrível de chocolate ou baunilha\n\nQuer um início de dia mais saudável e prático? Me chame! 🍫",
                'hashtags': "#NutraStart #ShakeNutritivo #CafeDaManhaSaudavel #ControleDePeso #4Life #RefeicaoCompleta"
            }
        },
        'tfboost': {
            'label': "🍊 TF Boost",
            'foto': 'AgACAgEAAxkBAAJI3WfpfL9H4PJfEoRHIpjU9kIcZalSAAJqrTEbGpNJR-o8369NrG-qAQADAgADeQADNgQ',
            'video': 'BAACAgEAAxkBAAIIFGb6s5IH0Ju1nA5yvoR6jr6WcFj7AAJzBAACp3zYR8lHRRUHAAGP8DYE',
            'documento': 'BQACAgEAAxkBAAIEtmb0dW3li1YSxQ51EDFbr6p_ReBRAAL7BAACtxWoR64zYiGCEo0NNgQ',
            'social_kit': {
                'story_image': 'PLACEHOLDER_STORY_IMAGE_TFBOOST',
                'feed_image': 'PLACEHOLDER_FEED_IMAGE_TFBOOST',
                'reels_video': 'PLACEHOLDER_REELS_VIDEO_TFBOOST',
                'copy_text': "🍊 Dê um BOOM de energia e imunidade no seu dia com TF Boost! 🍊\n\nSinta a vitalidade com esta bebida refrescante que combina o poder dos Fatores de Transferência com fontes naturais de energia como guaraná e chá verde. Perfeito para aqueles dias que exigem mais de você!\n\n✅ Energia sustentada sem picos\n✅ Rico em Vitamina C\n✅ Fortalece o sistema de defesa\n\nPrecisa de um gás extra? Experimente o TF Boost! ✨",
                'hashtags': "#TFBoost #EnergiaNatural #VitaminaC #Imunidade #4LifeBrasil #Foco #Vitalidade"
            }
        },
        'protf': {
            'label': "🏋️ PRO-TF",
            'foto': 'AgACAgEAAxkBAAJI-2fpoSVWLR0hXjd_joeMWTF1xu3CAAJkrTEb-9pRR7NVkptmq-v_AQADAgADeQADNgQ',
            'video': 'BAACAgEAAxkBAAIHWWb5F38vaLmimEPwfMQv4YGjdbiYAAKhBAAC1BLBR-0l-PRdCObcNgQ',
            'documento': 'BQACAgEAAxkBAAI3GGdd-wbglUIZ6aUMduLIPS7V5qnvAAK0BAACpNXwRuDyEfOCCu_QNgQ',
            'social_kit': {
                'story_image': 'PLACEHOLDER_STORY_IMAGE_PROTF',
                'feed_image': 'PLACEHOLDER_FEED_IMAGE_PROTF',
                'reels_video': 'PLACEHOLDER_REELS_VIDEO_PROTF',
                'copy_text': "🏋️‍♂️ Transforme seu corpo e seus resultados com PRO-TF! 🏋️‍♀️\n\nA proteína mais avançada do mercado, que não só ajuda a construir massa muscular magra, mas também estimula o metabolismo e fortalece o sistema imunológico.\n\n✅ Constrói e protege a massa muscular\n✅ Acelera a queima de gordura\n✅ Delicioso sabor de baunilha ou chocolate\n\nEleve seu treino e sua saúde a um novo patamar. Fale comigo! 💪",
                'hashtags': "#PROTF #Proteina #MassaMuscular #QueimaDeGordura #Fitness #4LifeFit #Treino"
            }
        },
        'colageno': {
            'label': "✨ Collagen",
            'foto': 'AgACAgEAAxkBAAJI5WfpffsHwNx_i3waE3tg9UxaJ64MAAJtrTEbGpNJR7nlMy_PL0kmAQADAgADeQADNgQ',
            'video': 'BAACAgEAAxkBAAIF7Gb35IcC8AxJ-ScYp1AAAb1rJLSRkAACngQAApNduUcrNi_XyyZ5BDYE',
            'documento': 'BQACAgEAAxkBAAI4nmdmtA60860qO0S8oVmgkXM5pO6sAALLBAACaqU5RwqVHw4I3chiNgQ',
            'social_kit': {
                'story_image': 'PLACEHOLDER_STORY_IMAGE_COLLAGEN',
                'feed_image': 'PLACEHOLDER_FEED_IMAGE_COLLAGEN',
                'reels_video': 'PLACEHOLDER_REELS_VIDEO_COLLAGEN',
                'copy_text': "✨ Revele sua melhor versão com o Colágeno 4Life! ✨\n\nNossa fórmula exclusiva não cuida apenas da sua pele, mas também fortalece cabelos, unhas e articulações, tudo isso enquanto reforça seu sistema imunológico com Fatores de Transferência.\n\n✅ Melhora a elasticidade e hidratação da pele\n✅ Fortalece unhas e cabelos\n✅ Suporte para a saúde das articulações\n\nBeleza que vem de dentro para fora. Vamos conversar sobre seus benefícios! 💖",
                'hashtags': "#Colageno4Life #PeleRadiante #CabelosFortes #ArticulacoesSaudaveis #BelezaDeDentroParaFora #4Life"
            }
        },
        'glutamineprime': {
            'label': "🔬 Glutamine Prime",
            'foto': 'AgACAgEAAxkBAAJI6mfpfjRVQDz12l9jfEeLTv9TOusaAAJvrTEbGpNJR56RpgVLJFPpAQADAgADeQADNgQ',
            'video': 'BAACAgEAAxkBAAIWjmcIfIMTskdTF3V_KmOotze7gqdeAALOBAACynwwRARdX5BQ54SPNgQ',
            'documento': 'BQACAgEAAxkBAAIWkGcIfS4NVmA9kOU0cj7Fj6LKdv50AAICBQACTQpBRG2aA-lUC6N-NgQ',
            'social_kit': {
                'story_image': 'PLACEHOLDER_STORY_IMAGE_GLUTAMINE',
                'feed_image': 'PLACEHOLDER_FEED_IMAGE_GLUTAMINE',
                'reels_video': 'PLACEHOLDER_REELS_VIDEO_GLUTAMINE',
                'copy_text': "🔬 Dê o combustível que suas células de defesa precisam com Glutamine Prime! 🔬\n\nA glutamina é um aminoácido vital para a recuperação e o bom funcionamento do sistema imunológico. Nossa fórmula é potencializada com NanoFactor® para uma comunicação celular mais eficiente.\n\n✅ Combustível para as células imunes\n✅ Auxilia na recuperação pós-exercício\n✅ Suporte nutricional avançado\n\nOtimize sua saúde a nível celular. Quer saber mais? Me chame! 👨‍🔬",
                'hashtags': "#GlutaminePrime #Recuperacao #SaudeCelular #Imunidade #NanoFactor #4Life"
            }
        },
        'tfmastigavel': {
            'label': "🍊 TF Mastigável",
            'foto': 'AgACAgEAAxkBAAJI7mfpfm_opqE5aP3S9lrBVLKwsKp3AAJwrTEbGpNJR11OgLJD2wPAAQADAgADeQADNgQ',
            'video': 'BAACAgEAAxkBAAI4zmdocXrHaVWPQP1cwblA1ANMPu7wAAJCBgACgvBIRw2goJ75LdDkNgQ',
            'documento': 'BQACAgEAAxkBAAI45WdoeZ-bTPJUtsn1s8RVUSLNkpv1AAIYBAAC80lIRxRRAwAB5DCZhjYE',
            'social_kit': {
                'story_image': 'PLACEHOLDER_STORY_IMAGE_MASTIGAVEL',
                'feed_image': 'PLACEHOLDER_FEED_IMAGE_MASTIGAVEL',
                'reels_video': 'PLACEHOLDER_REELS_VIDEO_MASTIGAVEL',
                'copy_text': "🍊 Cuidar da imunidade das crianças (e dos adultos!) nunca foi tão gostoso! 🍊\n\nO TF Mastigável oferece o suporte inteligente do Tri-Factor Formula em um tablete com delicioso sabor cítrico. A forma divertida e eficaz de manter as defesas da família sempre em alta.\n\n✅ Suporte imunológico para todas as idades\n✅ Sabor que as crianças adoram\n✅ Prático e fácil de consumir\n\nProteção e sabor para quem você ama. Peça o seu! ❤️",
                'hashtags': "#TFMastigavel #ImunidadeInfantil #SaudeDaFamilia #4LifeKids #FatoresDeTransferencia"
            }
        }
    }
}

# --- Textos de Pitch de Venda (para o botão "Pitch de Venda" original) ---
PITCH_DE_VENDA_TEXT = {
    'riovidaburst': """🫐 *RioVida Burst 4Life*: Saúde e sabor! 💥

Sinta o poder dos antioxidantes e Transfer Factors em cada sachê, apoiando seu corpo e aumentando sua energia:

1️⃣ *Imunidade Reforçada:* Aumente a sua resistência, promovendo mais saúde.
2️⃣ *Energia Sem Limites:* Diga adeus ao cansaço, aproveitando cada momento com mais disposição.
3️⃣ *Proteção Antioxidante:* Neutralize os radicais livres, mantendo a sua pele com aparência jovem.
4️⃣ *Bem-Estar Completo:* Melhore o seu humor, fortaleça o seu corpo e sinta-se no auge da sua forma física e mental.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), açaí, blueberry, sabugueiro, uva e romã.

*Modo de tomar:* Consuma um sachê ao dia.

*RioVida Burst*: A sua dose diária de saúde e energia! 🫐
""",
    'riovidastix': """🍷🍇 *RioVida Stix 4Life*: Refrescância e imunidade! 🍷

Transforme a sua água em uma aliada da sua saúde com esta combinação de Transfer Factor e antioxidantes:

1️⃣ *Defesa Imunológica:* Fortaleça o seu sistema imunológico.
2️⃣ *Hidratação Turbinada:* Refresque-se com o sabor de frutas vermelhas.
3️⃣ *Praticidade Imbatível:* Leve os seus sticks para onde quiser.
4️⃣ *Proteção Celular:* Neutralize os radicais livres e promova o bem estar.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), vitamina C, extrato de romã, açaí e blueberry.

*Modo de tomar:* Misture um stick em 500ml de água. Consuma uma vez ao dia.

*RioVida Stix*: A maneira mais prática de cuidar da sua saúde! 🍷🍇
""",
    'bioefa': """🌿 *BioEFA 4Life*: Um corpo em equilíbrio! 🌿

Nutra o seu organismo com os ácidos graxos essenciais que ele precisa para funcionar:

1️⃣ *Coração Saudável:* Cuide da sua saúde cardiovascular.
2️⃣ *Cérebro Ativo:* Melhore a sua memória e concentração.
3️⃣ *Imunidade Fortalecida:* Equilibre a resposta inflamatória.
4️⃣ *Pele Radiante:* Hidrate e proteja a sua pele.

*Ingredientes Principais:* Óleo de peixe, óleo de linhaça e óleo de borragem.

*Modo de tomar:* Tome duas (2) cápsulas softgel ao dia, com 240ml de líquido.

*BioEFA*: Uma vida mais longa e saudável! 🌿
""",
    'energygostix': """⚡ *Energy Go Stix 4Life*: Energia e foco! ⚡

Transforme o seu dia com esta explosão de sabor e vitalidade, que te ajuda a superar o cansaço:

1️⃣ *Energia Instantânea:* Sinta um impulso imediato de energia.
2️⃣ *Foco Implacável:* Aumente a sua concentração e clareza mental.
3️⃣ *Proteção Antioxidante:* Defenda as suas células contra os radicais livres.
4️⃣ *Praticidade Absoluta:* Leve os seus sticks para onde quiser.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), chá verde, guaraná, vitaminas do complexo B.

*Modo de tomar:* Dissolva um stick em 240ml de água. Consuma uma vez ao dia.

*Energy Go Stix*: Um dia produtivo e cheio de energia! ⚡
""",
    'tfplus': """🐣🐄🍄🔝 *TF Plus 4Life*: A proteção imunológica! 🛡️

Dê ao seu sistema imunológico o suporte que ele precisa:

1️⃣ *Imunidade Potencializada:* Aumente a atividade das suas células de defesa.
2️⃣ *Bem-Estar Integral:* Sinta mais disposição e qualidade de vida.
3️⃣ *Proteção Celular Avançada:* Defenda as suas células contra os danos.
4️⃣ *Ingredientes Premium:* Desfrute de uma fórmula com ingredientes naturais.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), cogumelos maitake e shiitake, zinco, vitamina C.

*Modo de tomar:* Tome duas (2) cápsulas ao dia, com 240ml de líquido.

*TF Plus*: Uma vida mais saudável! 🛡️
""",
    'tfplus30caps': """💊 *TF Plus 30 Cápsulas 4Life*: Seu Reforço Imunológico Concentrado e Prático! ✨

A potência máxima do TF Plus, agora na conveniência de uma embalagem com 30 cápsulas. Ideal para quem busca experimentar os benefícios incríveis dos Fatores de Transferência ou precisa de uma solução compacta para manter a imunidade blindada em qualquer lugar.

1️⃣ *Imunidade Inteligente:* Fórmula avançada com Fatores de Transferência e o exclusivo blend Cordyvant™ para educar, fortalecer e equilibrar seu sistema de defesa.
2️⃣ *Praticidade Total:* Leve com você para viagens, trabalho ou para o dia a dia, garantindo sua dose de proteção.
3️⃣ *Resultados Comprovados:* Baseado na ciência dos Fatores de Transferência, que há décadas ajudam a promover saúde e bem-estar.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), blend Cordyvant™ (incluindo cogumelos maitake, shiitake, cordyceps, beta-glucanos e mais), Zinco.

*Modo de tomar:* Tome uma (1) cápsula ao dia com 240ml de líquido, ou conforme orientação profissional.

*TF Plus 30 Cápsulas*: A escolha inteligente para uma imunidade de ferro! 💪🛡️
""",
    'tfzinco': """🐣🐄 *TF Zinco 4Life*: Imunidade! 💪

Fortaleça o seu sistema imunológico com a combinação de Transfer Factor e Zinco:

1️⃣ *Defesas Blindadas:* Aumente a sua resistência.
2️⃣ *Pele Radiante:* Cuide da saúde da sua pele.
3️⃣ *Ação Antioxidante:* Proteja as suas células contra os radicais livres.
4️⃣ *Suporte Nutricional Essencial:* Garanta o aporte de Zinco.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), Zinco.

*Modo de tomar:* Tome um (1) tablete ao dia, com 240ml de líquido.

*TF Zinco*: Imunidade e bem-estar! 💪
""",
    'nutrastart': """🥤🍽️ *NutraStart 4Life*: O café da manhã ideal! ☀️

Comece o seu dia com energia, vitalidade e todos os nutrientes que você precisa:

1️⃣ *Nutrição Completa:* Desfrute de um shake equilibrado, rico em proteínas, fibras, vitaminas e minerais.
2️⃣ *Imunidade Fortalecida:* Reforce o seu sistema imunológico.
3️⃣ *Controle de Peso Inteligente:* Alcance os seus objetivos.
4️⃣ *Praticidade Sem Igual:* Prepare o seu shake em segundos.

*Ingredientes Principais:* Proteína de soro do leite, fibra de aveia, 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), vitaminas e minerais.

*Modo de tomar:* Misture um scoop em 240ml de água ou leite. Consuma no café da manhã ou como substituto de refeição.

*NutraStart*: Um dia produtivo e cheio de energia! ☀️
""",
    'protf': """🏋️‍♂️💪 *PRO-TF 4Life*: A proteína que redefine os seus limites! 🚀

Alcance resultados com esta fórmula para te ajudar a construir músculos e elevar o seu desempenho:

1️⃣ *Músculos Poderosos:* Estimule a síntese proteica e maximize o ganho de massa muscular.
2️⃣ *Queima de Gordura Acelerada:* Turbine o seu metabolismo.
3️⃣ *Desempenho Imbatível:* Aumente a sua força e resistência.
4️⃣ *Imunidade Blindada:* Fortaleça o seu sistema imunológico.

*Ingredientes Principais:* Proteína do soro do leite hidrolisada, proteína do ovo hidrolisada, 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo).

*Modo de tomar:* Misture um scoop em 240ml de água ou sua bebida preferida após o treino ou quando precisar de um aporte proteico.

*PRO-TF*: Uma saúde inabalável! 🚀
""",
    'colageno': """💧🌟 *Transfer Factor Collagen da 4Life*: A beleza e bem-estar em um só suplemento! ✨

Esta fórmula exclusiva combina colágeno hidrolisado com Transfer Factors, vitaminas e antioxidantes:

1️⃣ *Pele Radiante:*
  • 💧 Aumenta a hidratação e a elasticidade.
  • 🔄 Estimula a regeneração celular, apoiando a saúde da pele.

2️⃣ *Articulações Flexíveis:*
  • 🦴 Fortalece as cartilagens, proporcionando conforto e mobilidade.
  • 🤕 Alivia desconfortos, permitindo movimentação livre.

3️⃣ *Cabelos e Unhas Saudáveis:*
  • 💇‍♀️ Fortalece os fios.
  • 💅 Deixa as unhas mais fortes.

4️⃣ *Um Corpo Revitalizado:*
  • 🦴💪 Fortalece os ossos e músculos.
  • 🛡️ Reforça o sistema imunológico.

*Ingredientes Principais:* Colágeno hidrolisado, 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), Vitamina C, Biotina, Vitamina E.

*Modo de tomar:* Misture um scoop em 240ml de água ou sua bebida preferida. Consuma uma vez ao dia.

Transforme a sua saúde e bem estar com *Transfer Factor Collagen*! ✨
""",
    'tfboost': """🍊✴️ *TF Boost 4Life*: Desperte a sua energia interior! 🌟

Revitalize o seu corpo e mente com esta fórmula, que combina Transfer Factor, antioxidantes e ingredientes energizantes:

1️⃣ *Energia Infinita:* Sinta energia, mantendo você ativo.
2️⃣ *Foco Laser:* Melhore a sua concentração e clareza mental.
3️⃣ *Proteção Antioxidante Avançada:* Defenda as suas células contra os radicais livres.
4️⃣ *Suporte Imunológico Completo:* Reforce o seu sistema imunológico.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), guaraná, chá verde, vitamina C, acerola.

*Modo de tomar:* Dissolva um sachê em 240ml de água. Consuma uma vez ao dia.

*TF Boost*: Vitalidade! 🌟
""",
    'glutamineprime': """⛽⚡🔬 *4Life NanoFactor Glutamine Prime* é o segredo para um sistema imunológico forte! 😎

A glutamina é um aminoácido essencial para a saúde das suas células de defesa. Descubra como este suplemento pode otimizar sua imunidade:

✨ *Combustível para a Imunidade:* Fornece energia para as células do sistema imunológico, aumentando sua capacidade de combater agressores.
✨ *Reparação e Crescimento:* Auxilia na síntese de DNA e proteínas, importantes para a manutenção celular e recuperação.
✨ *Proteção Integral:* Fortalece as barreiras do seu corpo, auxiliando a manter a integridade celular.

*Ingredientes Principais:* Glutamina, NanoFactor® (concentrado de ultrafiltração de proteínas do soro do leite de vaca e gema de ovo de galinha).

*Modo de tomar:* Misture um sachê em 240ml de água ou sua bebida preferida. Consuma uma vez ao dia.

Invista em *4Life NanoFactor Glutamine Prime* e sinta a diferença!
""",
    'tfmastigavel': """🍊🟠 *TF Mastigável 4Life*: Imunidade com sabor! 😄

Proteja a saúde dos seus filhos com estes tabletes mastigáveis que combinam Transfer Factor:

1️⃣ *Defesas Fortificadas:* Aumente a sua resistência.
2️⃣ *Sabor Irresistível:* Transforme a suplementação em um momento prazeroso.
3️⃣ *Praticidade Para o Dia a Dia:* Leve os tabletes para onde quiser.
4️⃣ *Saúde Para Toda a Família:* Cuide da imunidade de todos.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), vitamina C, acerola.

*Modo de tomar:* Mastigue dois (2) tabletes ao dia. Para crianças menores, esmague o tablete e misture com a comida.

*TF Mastigável*: Proteção! 😄
"""
}


# --- DADOS ADICIONAIS NECESSÁRIOS PARA OUTROS MÓDULOS ---

CONVITES_TEXT = {
    'convite_1': "📈 Convite Profissional\n\nOi [Nome do Convidado], como vai? Estou a expandir um projeto na área de bem-estar e tecnologia e lembrei-me de si pelo seu perfil dinâmico. Gostaria de apresentar uma oportunidade que pode ser do seu interesse. Podemos conversar por 15 minutos esta semana?",
    'convite_2': "😊 Convite Amigável\n\nE aí, [Nome do Convidado]! Tudo bem? Estou a trabalhar em algo novo e super empolgante que acho que tem tudo a ver consigo. Que tal um café (virtual ou não) para eu te contar as novidades? Sem compromisso!",
    'convite_3': "🌍 Convite Flexível\n\nOlá, [Nome do Convidado]. Vi que você busca novas oportunidades com flexibilidade. Estou a desenvolver um negócio que permite trabalhar de qualquer lugar e com horários flexíveis. Se tiver interesse em saber mais, me diga qual o melhor horário para uma breve chamada.",
    'convite_4': "💵 Convite de Renda Extra\n\nOi, [Nome do Convidado]! Você já pensou em ter uma fonte de renda extra que não atrapalhe sua atividade principal? Encontrei uma forma inteligente de fazer isso e gostaria de compartilhar consigo. Tem um momento para conversarmos sobre?",
    'convite_14': "🎁 Convite de Oportunidade\n\nOlá, [Nome do Convidado]. Sinto que você é uma pessoa que está sempre aberta a novas oportunidades. Tenho algo em mãos que pode ser exatamente o que você procura para o seu futuro. Gostaria de saber mais?",
    'convise_15': "💡 Convite de Solução\n\nOi, [Nome do Convidado]. Muitas pessoas estão a procurar soluções para [mencionar um problema, ex: ter mais tempo, mais segurança financeira]. Estou a trabalhar com uma solução que tem ajudado muita gente nessa área. Se isto faz sentido para si, vamos conversar."
}

GLOSSARIO_TERMS = {
    'upline': '**🔝 Upline:** A linha de distribuidores acima de você na organização, que o apoiam e orientam.',
    'downline': '**👥 Downline:** A rede de distribuidores que você pessoalmente patrocinou e que foram patrocinados por eles.',
    'pv': '**Pessoais (PV):** Pontos de Volume gerados pelas suas compras pessoais de produtos.',
    'vo': '**Organizacional (VO):** Pontos de Volume totais gerados por toda a sua downline.',
    'lp': '**Pontos de Lealdade (LP):** Pontos que você ganha através do Programa de Lealdade, que podem ser trocados por produtos.'
}

POSITIONS = {
    "Associado": {
        "emoji": "🔹",
        "nivel_categoria": "Nível Inicial",
        "pv_mensal": 50,
        "linhas_qualificadas": None,
        "vo_rede": 0,
        "media_ganho": 50.00
    },
    "Construtor": {
        "emoji": "🔸",
        "nivel_categoria": "Nível Inicial",
        "pv_mensal": 100,
        "linhas_qualificadas": [{"quantidade": 3, "posicao": "Associado"}],
        "vo_rede": 0,
        "media_ganho": 200.00
    },
    "Diamante": {
        "emoji": "💎",
        "nivel_categoria": "Liderança",
        "pv_mensal": 100,
        "linhas_qualificadas": [{"quantidade": 6, "posicao": "Construtor"}],
        "vo_rede": 3000,
        "media_ganho": 1000.00
    },
    "Presidencial": {
        "emoji": "⭐",
        "nivel_categoria": "Liderança",
        "pv_mensal": 100,
        "linhas_qualificadas": [{"quantidade": 8, "posicao": "Diamante"}],
        "vo_rede": 10000,
        "media_ganho": 5000.00
    }
}

YOUTUBE_LINKS = [
    ("Canal Oficial 4Life", "https://www.youtube.com/c/4lifeoficial"),
    ("Canal Equipe de Triunfo", "https://www.youtube.com/c/EquipedeTriunfo")
]
TELEGRAM_LINKS = [
    ("Grupo de Suporte", "https://t.me/seu_grupo_de_suporte"),
    ("Canal de Notícias", "https://t.me/seu_canal_de_noticias")
]
WHATSAPP_LINKS = [
    ("Grupo WhatsApp Principal", "https://chat.whatsapp.com/seu_grupo"),
]

