# NOME DO ARQUIVO: features/products/data.py
# REFACTOR: Centraliza todos os file_ids de mídias e textos de pitch de venda.

MEDIA = {
    'bonusconstrutormidias': {
        'video1': 'BAACAgEAAxkBAAJAU2fGAtnueBNRnb1LCqFFFfHG35OYAAJcBQACS1kxRuel2nL4TjefNgQ',
        'documento': 'BQACAgEAAxkBAAJAVWfGBGDBfHcAAXBT7LRKfZTnTKNG7QACYAUAAktZMUbZVJlfL5F_9jYE'
    },
    'fatorestransf': {
        'video1': {'type': 'video', 'id': 'BAACAgEAAxkBAAJJMGfqtNj0QxKXG4FOpQS95NmJXcupAAJKBgAC-9pZR5ORbjj6QwSVNgQ'},
        'video2': {'type': 'video', 'id': 'BAACAgEAAxkBAAJB8WfOAhRPVUK8u9LxuB-BSIXDPfTKAALSBAACynwwRMxkekB46LmzNgQ'},
        'video3': {'type': 'video', 'id': 'BAACAgEAAxkBAAIyi2c7eP1__N6H9Wwz0iWXMrOx6BwqAAJTBAACI1_ZRc1ewElkbwT5NgQ'},
        'table': {'type': 'document', 'id': 'BQACAgEAAxkBAAIw6Gc4xcpWr6KivsAiGUwOpwcID0wxAALjBAAChl_IRdQoqw0PYFCgNgQ'},
        'video4': {'type': 'video', 'id': 'BAACAgEAAxkBAAIyyWc8aKjKjrsGLMDoDBBrR-HFDfSYAALLBAACI1_hRZYG61y0muUdNgQ'},
        'ft1': {'type': 'video', 'id': 'BAACAgEAAxkBAAI112dUNHWThBk3iHGYYOLi5iC5LvaCAAL4BAAC03ygRhy6g836KRDpNgQ'},
        'capsula': {'type': 'video', 'id': 'BAACAgEAAx0CfAGLsgACRxhno4SQEokUnApAOVPROj7qYDFNXAACmAQAAlRQGEX4V0FoWwHq-DYE'}
    },
    'fabrica4life': {
        'armazem': 'BAACAgEAAxkBAAIBMGbncmJda7Sz-CPPc4unHFYjinjdAAK6CwACz0RBR_6nHEgo0YTmNgQ',
        'envase': 'BAACAgEAAxkBAAIBMmbndcrrkMOWppQGRixAh_CbE4oeAAK7CwACz0RBRypfMI6d_CjQNgQ',
        'novafabrica': [
            'BAACAgEAAxkBAAIBNGbndj-Sl43gh_kdQLBXKhkqSc6AAAK8CwACz0RBR6FFUzlAx6JANgQ',
            'BAACAgEAAxkBAAI7xGecqaiH-DF6hsXXxCIbFqoflWfpAAIyBQACNtvoRLvspG4xWX98NgQ'
        ]
    },
    'folheteria': {
        'panfletoprodutosnovo': 'BQACAgEAAxkBAAIhW2cdTj5i9HqUKjzciT-waYnZUIj0AAIOBQACw_vpRCemtnyqP0xmNgQ',
        'panfletonovo4life': 'BQACAgEAAxkBAAI1uGdTRi6Fn0EzL5Evyxuppj2xiIQsAAKABQAC4GeZRnrKvfp-PB31NgQ'
    },
    'catalogoprodutos': {
        'documento': 'BQACAgEAAxkBAAIxj2c45EdaH76knO_Xm1drcy3S4uqGAAL0BAAChl_IRZzzUO7vIgo4NgQ'
    },
    'enqueteimunidade': {
        'id': 'BQACAgEAAxkBAAI1zmdUMEqyrMmahlNpTxJGe-eKJ4ehAAL3BAAC03ygRi9sfVM-P6H_NgQ'
    },
    'glossario': {
        'documento': 'BQACAgEAAxkBAANdZuXtiawdQU-i5AABuz6AeHO897IkAAL1AwACmLwwR79WaVrxRlUINgQ'
    },
    'recompensas2024': {
        'documento': 'BQACAgEAAxkBAANJZuXs2N0BGNgYFLeOGs0btJjgYkEAAvEDAAKYvDBHHRLaoQgyoHU2BA'
    },
    'planotrabalho90dias': {
        'pdf': 'BQACAgEAAxkBAANXZuXtZG2ZHLUjyXFzvmpc32A0m28AAvQDAAKYvDBHeMndEw69BD02BA',
        'ppt': 'BQACAgEAAxkBAAIDa2bpX_0PhR7Iq9vZNaUmfRLxv4pjAALJBAACNzRIR5jQpmV2G0XjNgQ'
    },
     'marketing_rede': {
        "video": "BAACAgEAAxkBAAIxpmc46CYHNY8qufZwAXQXw7z7eAspAAL2BAAChl_IRf-DsXQNjmvONgQ"
    },
    'fidelidade_video': {
        "id": "BAACAgEAAxkBAAI7hWeXY1Qa7JJGXSCbf-zMO3PJpvWdAAKABQAC32i4RISCLL2YG-mLNgQ"
    },
    'beneficioriovidaburst': {
        'video': 'BAACAgEAAxkBAAJUX2iXLsqb7Xov4heg8nOpkgAB7jXg8wAC-wUAAp6JuUSAbsjdTnY92zYE',
        'documento': 'BQACAgEAAxkBAAMxZt4kyxybDpyStV695_x9BqHi-gUAAp0DAAJbOfFGNpvdNZiPoXc2BA',
        'perfil_mobile': 'AgACAgEAAxkBAAJIw2fpaw-kaCGnsMvkQ7_-n_5e1KNQAAJArTEbGpNJR71s3kcAAXAnIgEAAwIAA3kAAzYE',
        'video1': 'BAACAgEAAxkBAAI47WdpTKbF0E2-rEWQvdQsCPIGaN72AAJ0BQACDvtJR2anqfFkdCB_NgQ',
        'recorte_png': 'BQACAgEAAxkBAAI_6mfEt79OV841CKg3G7U2osKjHXidAAIbBAACi5sgRtDOVXkYSc8kNgQ',
        'imagens_detalhadas': {
            'rvb_img_1': {'nome_botao': '📷 Imagem #1', 'file_id': 'AgACAgEAAxkBAAJUa2iXgYsehHQXtRRTBPUddokxa4nmAAITsTEbnom5RDOFLibyCrB7AQADAgADeAADNgQ'},
            'rvb_img_2': {'nome_botao': '📷 Imagem #2', 'file_id': 'AgACAgEAAxkBAAJUbWiXghGphXpiaz-ZpW-0dyl3_MpwAAIUsTEbnom5RMDUyyNDiqISAQADAgADeQADNgQ'},
        },
        'carrosseis': {
            'rvb_car_1': {'nome_botao': '🎠 Carrossel #1', 'file_ids': ['PLACEHOLDER_RVB_C1_IMG1']},
            'rvb_car_2': {'nome_botao': '🎠 Carrossel #2', 'file_ids': ['PLACEHOLDER_RVB_C2_IMG1', 'PLACEHOLDER_RVB_C2_IMG2']},
        }
    },
    'beneficioriovidastix': {
        'video': 'BAACAgEAAxkBAAJBSmfGPZK4y6Yq5XNuodprmReqbhWjAAJzBQACS1kxRoWhJ5c0q9C0NgQ',
        'video1': 'BAACAgEAAxkBAAJBSGfGPNcqHlEzVGu4MFXkVCeHzCrLAAJyBQACS1kxRhmzw99zJ05uNgQ',
        'documento': 'BQACAgEAAx0CfAGLsgACCPRm9B5_NQTLMkliTyY38WGKPbzWPgACfwQAAqQtoUdHteDxrzz-jDYE',
        'perfil_mobile': 'AgACAgEAAxkBAAJIw2fpaw-kaCGnsMvkQ7_-n_5e1KNQAAJArTEbGpNJR71s3kcAAXAnIgEAAwIAA3kAAzYE',
        'recorte_png': 'BAACAgEAAxkBAAI_8GfEuOYZhNG-hTe5QQ97uZC1PVgIAAIeBAACi5sgRqAL-5kEKcnpNgQ',
        'imagens_detalhadas': {
            'rvs_img_1': {'nome_botao': '📷 Imagem #1', 'file_id': 'AgACAgEAAxkBAAJPbmgzNgToTi1BSLHEfjSkJUbkp8z1AAJarjEbp3-YRS-ZYpO590cxAQADAgADeQADNgQ'},
            'rvs_img_2': {'nome_botao': '📷 Imagem #2', 'file_id': 'PLACEHOLDER_RVS_IMG2'},
        },
        'carrosseis': {
            'rvs_car_1': {'nome_botao': '🎠 Carrossel #1', 'file_ids': ['PLACEHOLDER_RVS_C1_IMG1']},
        }
    },
    'beneficiobioefa': { 
        'video': 'BAACAgEAAxkBAAJPSmgyl2euQMx0brhHHHxgN9sVWb8IAAL_BAACp3-QRd8S7iFF1DKQNgQ',
        'video1': 'BAACAgEAAxkBAAIBGmbnb4LTK5V2ulGbaDjwHFK4OfIaAAK3CwACz0RBR4af4DnRtfcuNgQ',
        'video2': 'BAACAgEAAxkBAAIBHGbnb7uIRh8tcr1l47qzDp9R6ZdfAAK4CwACz0RBR_LZ6Y0Ux6-eNgQ',
        'video3': 'BAACAgEAAxkBAAI3SmdeBUHlIS7ZxYX9v4SC8dCVSAQ3AAKlBQACPoiBRzwlaYje4BLNNgQ',
        'documento': 'BQACAgEAAxkBAAJDmWfY5EKUqzRUd93IGl95fZiZCK8jAAIwBAAC55rIRot5b1n-bCGKNgQ',
        'perfil_mobile': 'AgACAgEAAxkBAAJIuGfpaff9kWF09Y3UfOSPx5iTLN4PAAI1rTEbGpNJRxv12_knzg0BAQADAgADeQADNgQ',
        'documento2': 'BQACAgEAAxkBAAI4XWdjcM8HciMXlTZVZO3iskLlz9uEAAKZBAAC8vEYR3UBKqKmzW22NgQ',
        'recorte_png': 'BQACAgEAAxkBAAJAA2fEu_fpAQ4gKevh0CoIGcQRcIWnAAIjBAACi5sgRlEXJyysFTE_NgQ',
        'imagens_detalhadas': {
            'bio_img_1': {'nome_botao': '📷 Imagem #1', 'file_id': 'PLACEHOLDER_BIO_IMG1'},
            'bio_img_2': {'nome_botao': '📷 Imagem #2', 'file_id': 'PLACEHOLDER_BIO_IMG2'},
        },
        'carrosseis': {
            'bio_car_1': {
                'nome_botao': '🎠 Carrossel BioEFA #1', 
                'file_ids': [
                    'AgACAgEAAxkBAAJPpmgzQLQhKC1mhjH-UdcBqS84n-cuAAJerjEbp3-YRWPrO9_BoMBiAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPp2gzQLRel4THc7-F8HbolK3fIXusAAJfrjEbp3-YRQ_AjRq4hGrhAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPqGgzQLSW9nK5i3yhhIy5U5gKXwxMAAJgrjEbp3-YRXawtIb3ox8kAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPqWgzQLS8qTWn923R4MZ6Nhe03WkzAAJhrjEbp3-YRZj5D8m2bjixAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPqmgzQLRPl911PdLPyErJ3qnwTwSSAAJirjEbp3-YRSM-UV3ZRQzHAQADAgADeQADNgQ'
                ]
            },
            'bio_car_2': {'nome_botao': '🎠 Carrossel BioEFA #2', 'file_ids': ['PLACEHOLDER_BIO_C2_IMG1']}, 
        }
    },
    'beneficioenergygostix': {
        'video': 'BAACAgEAAxkBAAJUYWiXL7D1KBC-hKBm9WqMRKAyXc9XAAL-BQACnom5RBgycWAwtSjYNgQ',
        'documento': 'BQACAgEAAxkBAAMzZt4lSZsZzqZyVGKuz9eUKr7Vq2EAAp4DAAJbOfFG8zorKuHMfh82BA',
        'perfil_mobile': 'AgACAgEAAxkBAAJIy2fpbA57ndR7vG0J_MehK_shs20EAAJHrTEbGpNJR6TVL1LEoIJqAQADAgADeQADNgQ',
        'recorte_png': 'BAACAgEAAxkBAAI_8mfEuS7c2pW1lkENlEID_ZtSAv94AAIfBAACi5sgRhMOPDyJ251HNgQ',
        'imagens_detalhadas': {
            'eng_img_1': {'nome_botao': '📷 Imagem #1', 'file_id': 'PLACEHOLDER_ENG_IMG1'},
        },
        'carrosseis': {
            'eng_car_1': {'nome_botao': '🎠 Carrossel #1', 'file_ids': ['PLACEHOLDER_ENG_C1_IMG1']},
        }
    },
    'beneficiotfplus': {
        'video1': 'BAACAgEAAxkBAAICtmboFTTgNOCnGllv5Ff-5-914JOHAAIGCgACz0RJR8say1htm3VaNgQ',
        'video2': 'BAACAgEAAxkBAAICuGboFXcPOy5QJ8m-kPOGh09bMCh1AAIHCgACz0RJRxQpPD3Fa_rvNgQ',
        'documento': 'BQACAgEAAxkBAAICu2boFqVza6DHajduav8Bt9BewjnkAAIICgACz0RJR4CWyGtgxbNuNgQ',
        'perfil_mobile': 'AgACAgEAAxkBAAJIz2fpbIe8Z0ura7cnY-o12mJ7nKy3AAJIrTEbGpNJR2I6ds8Po1kTAQADAgADeQADNgQ',
        'recorte_png': 'BAACAgEAAxkBAAI_-GfEunZ4Pf4t6sJuQGKUMUdQ7rnJAAIiBAACi5sgRtTK4BXe8Q_xNgQ',
        'imagens_detalhadas': {
            'tfp_img_1': {'nome_botao': '📷 Imagem #1', 'file_id': 'PLACEHOLDER_TFP_IMG1'},
        },
        'carrosseis': {
            'tfp_car_1': { 
                'nome_botao': '🎠 Carrossel TFPlus #1',
                'file_ids': [
                    'AgACAgEAAxkBAAJPhGgzO1x-vc-tMzu8SvTV8zuEDtYCAAJbrjEbp3-YRfp_Z0bajjJkAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPhWgzO1ybmFc-ZyIxVfmNesfT1X5wAAJcrjEbp3-YRYi7kH11HaMFAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPhmgzO1znEChH5ToOPWLwo7VTKSVqAAJdrjEbp3-YRdvjqV-ID8lOAQADAgADeQADNgQ'
                ]
            },
             'tfp_car_2': { 
                'nome_botao': '🎠 Carrossel TFPlus #2',
                'file_ids': [
                    'AgACAgEAAxkBAAJPwGgzRTCxN0D9q7OueL99XapniUVvAAJjrjEbp3-YRQrVRO7d9uHRAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPwWgzRTCH6EgSJOCR185COIgdLa7hAAJkrjEbp3-YRaRa8qQWU-oXAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPwmgzRTDcMBF-YpVXRk0c0tsgSsmeAAJlrjEbp3-YRX5lNyCZvD0wAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPw2gzRTCRRPRElfZC5N6i_ljssHrsAAJmrjEbp3-YRaGTSYjxNwaIAQADAgADeQADNgQ'
                ]
            },
            'tfp_car_3': {
                'nome_botao': '🎠 Carrossel TFPlus #3', 
                'file_ids': [
                    'AgACAgEAAxkBAAJP1mgzSSo6Fh9KcqlD2jAuE16J--__AAJdsDEbeNqYReGspQAB9s9nPAEAAwIAA3kAAzYE',
                    'AgACAgEAAxkBAAJP12gzSSpoBDB-IVuW6_715PFBZzA0AAJorjEbp3-YRVBF1bS-yudfAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJP2GgzSSo1fvn1QRyRecwmd4FqYIErAAJprjEbp3-YRUSndAAB-TfuKgEAAwIAA3kAAzYE',
                    'AgACAgEAAxkBAAJP2WgzSSqd2ta5msYOJnqnLcsSnnbJAAJqrjEbp3-YRYZYutT_0V8EAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJP2mgzSSpIPqdI5H56ijIlRfWlyEZ6AAJesDEbeNqYRXlV1X-MUTT2AQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJP22gzSSpsrrAyMQK25135JOnEO8ywAAJfsDEbeNqYRRWCmhTD_aCXAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJP3GgzSSqegPEGNalzjioOXW--exXrAAJrrjEbp3-YRYa0jCyfhRnhAQADAgADeQADNgQ'
                ]
            },
            'tfp_car_4': {'nome_botao': '🎠 Carrossel TFPlus #4', 'file_ids': ['PLACEHOLDER_TFP_C4_IMG1']},
        }
    },
    'beneficiotfplus30caps': { 
        'video': 'BAACAgEAAxkBAAJPOWgyb0ZEEzLBgCZqfAm265l6Xxh0AALZBAACp3-QRWgz7-MrCY0NNgQ',
        'video1': 'PLACEHOLDER_VIDEO1_ID_TFPLUS30',
        'documento': 'PLACEHOLDER_DOCUMENTO_ID_TFPLUS30',
        'perfil_mobile': 'PLACEHOLDER_PERFILMOBILE_ID_TFPLUS30',
        'recorte_png': 'PLACEHOLDER_RECORTEPNG_ID_TFPLUS30',
        'imagens_detalhadas': {
            'tfp30_img_1': {'nome_botao': '📷 Imagem #1', 'file_id': 'AgACAgEAAyEFAASNSVRUAAIE5mgybu_TgvyRS614CG0vhPSEbw11AAIHrjEbtX-RRT-pYabHSFYlAQADAgADeQADNgQ'},
            'tfp30_img_2': {'nome_botao': '📷 Imagem #2', 'file_id': 'PLACEHOLDER_TFP30_IMG2'},
        },
        'carrosseis': {
            'tfp30_car_1': { 
                'nome_botao': '🎠 Carrossel 30cap #1', 
                'file_ids': [ 
                    'AgACAgEAAxkBAAJPhGgzO1x-vc-tMzu8SvTV8zuEDtYCAAJbrjEbp3-YRfp_Z0bajjJkAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPhWgzO1ybmFc-ZyIxVfmNesfT1X5wAAJcrjEbp3-YRYi7kH11HaMFAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPhmgzO1znEChH5ToOPWLwo7VTKSVqAAJdrjEbp3-YRdvjqV-ID8lOAQADAgADeQADNgQ'
                ]
            }
        }
    },
    'beneficiotfzinco': {
        'documento': 'BQACAgEAAxkBAAJD-WfaIbM6LYt8sjD-YhouWGpOsZrrAAL-AwACtxWgR04AAdqdDwaCXTYE',
        'perfil_mobile': 'AgACAgEAAxkBAAJI02fpbK-_ZDexRnc3YzDeKDGms_mQAAJJrTEbGpNJR1EGLzdAaKE2AQADAgADeQADNgQ',
        'documento2': 'BQACAgEAAxkBAAI4N2djXcjiBG0DRfwKXWskVbNWwgAB9QACkQQAAvLxGEehlEd27kbO3TYE',
        'video': 'BAACAgEAAxkBAAI7qWeaTq2zU48iBsEtLdJOOCNL2f8QAAKZBwACL8jQRM8VaZzyHN22NgQ',
        'recorte_png': 'BAACAgEAAxkBAAI_5mfEtxsvKgiPEzmhbJErVkQPzT2ZAAIZBAACi5sgRpfrjJ0dRo9GNgQ',
        'imagens_detalhadas': {
            'tfz_img_1': {'nome_botao': '📷 Imagem #1', 'file_id': 'PLACEHOLDER_TFZ_IMG1'},
            'tfz_img_2': {'nome_botao': '📷 Imagem #2', 'file_id': 'PLACEHOLDER_TFZ_IMG2'},
        },
        'carrosseis': {
            'tfz_car_1': {
                'nome_botao': '🎠 Carrossel #1',
                'file_ids': [
                    'AgACAgEAAxkBAAJPVWgzK3oHlMztAr7cxQsWNejwZmwEAAJVrjEbp3-YRYH181iCE1kNAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPVmgzK3rI1tgpRZkmE1K6N284MsLmAAJWrjEbp3-YRRtYhFBXtB4fAQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPV2gzK3rfVzvZkLaH2wyiAwtsFuLcAAJXrjEbp3-YRU6Fv9NXuwi_AQADAgADeQADNgQ',
                    'AgACAgEAAxkBAAJPWGgzK3qrOQvdwKeSn9VeBtdtYmymAAJYrjEbp3-YReN7ysU4_9ZkAQADAgADeQADNgQ'
                ]
            },
            'tfz_car_2': {'nome_botao': '🎠 Carrossel #2', 'file_ids': ['PLACEHOLDER_TFZ_C2_IMG1']},
        }
    },
    'beneficionutrastart': {
        'video': 'BAACAgEAAxkBAAIDg2bpZaLV-92rwmxh78pNb9BPXTLPAALKBAACNzRIRwqUwDWOqKb8NgQ',
        'documento': 'BQACAgEAAxkBAAIDhWbpZ0BRUjZluUdXfzEZ0L4hV-vyAALLBAACNzRIR22E4cGkGvHoNgQ',
        'perfil_mobile': 'AgACAgEAAxkBAAJI12fpbOCMcR3xZwx-ENLIWWmg-pYKAAJKrTEbGpNJR2HM_u4rWwytAQADAgADeQADNgQ',
        'recorte_png': 'BAACAgEAAxkBAAI_9GfEuYu81YJXMV5flltP-63-mSYSAAIgBAACi5sgRhNgIZYq4wvrNgQ',
        'imagens_detalhadas': {
            'nut_img_1': {'nome_botao': '📷 Imagem #1', 'file_id': 'PLACEHOLDER_NUT_IMG1'},
        },
        'carrosseis': {
            'nut_car_1': {'nome_botao': '🎠 Carrossel #1', 'file_ids': ['PLACEHOLDER_NUT_C1_IMG1']},
        }
    },
    'beneficiotfboost': {
        'video': 'BAACAgEAAxkBAAIIFGb6s5IH0Ju1nA5yvoR6jr6WcFj7AAJzBAACp3zYR8lHRRUHAAGP8DYE',
        'documento': 'BQACAgEAAxkBAAIEtmb0dW3li1YSxQ51EDFbr6p_ReBRAAL7BAACtxWoR64zYiGCEo0NNgQ',
        'perfil_mobile': 'AgACAgEAAxkBAAJI3WfpfL9H4PJfEoRHIpjU9kIcZalSAAJqrTEbGpNJR-o8369NrG-qAQADAgADeQADNgQ',
        'recorte_png': 'BAACAgEAAxkBAAI_5GfEtmnrQjBCfrcU50jeO4T7E4fVAAIYBAACi5sgRhcpWWzi9zfmNgQ',
        'imagens_detalhadas': {
            'tfb_img_1': {'nome_botao': '📷 Imagem #1', 'file_id': 'PLACEHOLDER_TFB_IMG1'},
        },
        'carrosseis': {
            'tfb_car_1': {'nome_botao': '🎠 Carrossel #1', 'file_ids': ['PLACEHOLDER_TFB_C1_IMG1']},
        }
    },
    'beneficioprotf': {
        'video': 'BAACAgEAAxkBAAIHWWb5F38vaLmimEPwfMQv4YGjdbiYAAKhBAAC1BLBR-0l-PRdCObcNgQ',
        'documento': 'BQACAgEAAxkBAAI3GGdd-wbglUIZ6aUMduLIPS7V5qnvAAK0BAACpNXwRuDyEfOCCu_QNgQ',
        'perfil_mobile': 'AgACAgEAAxkBAAJI-2fpoSVWLR0hXjd_joeMWTF1xu3CAAJkrTEb-9pRR7NVkptmq-v_AQADAgADeQADNgQ',
        'recorte_png': 'BAACAgEAAxkBAAI_7GfEuA28pXol2n8f3lL1satlVrptAAIcBAACi5sgRqX4fFtXwgG0NgQ',
        'imagens_detalhadas': {
            'pro_img_1': {'nome_botao': '📷 Imagem #1', 'file_id': 'PLACEHOLDER_PRO_IMG1'},
            'pro_img_2': {'nome_botao': '📷 Imagem #2', 'file_id': 'PLACEHOLDER_PRO_IMG2'},
        },
        'carrosseis': {
            'pro_car_1': {'nome_botao': '🎠 Carrossel #1', 'file_ids': ['PLACEHOLDER_PRO_C1_IMG1']},
        }
    },
    'beneficiocolageno': {
        'video': 'BAACAgEAAxkBAAIF7Gb35IcC8AxJ-ScYp1AAAb1rJLSRkAACngQAApNduUcrNi_XyyZ5BDYE',
        'video1': 'BAACAgEAAxkBAAIXwWcOcMQR-fS1KNTlj-Z1cFblAZzrAAJiCwACAhOYRgV6N835_vTcNgQ',
        'documento': 'BQACAgEAAxkBAAI4nmdmtA60860qO0S8oVmgkXM5pO6sAALLBAACaqU5RwqVHw4I3chiNgQ',
        'documento1': 'BQACAgEAAxkBAAI4n2dmtA6fAAFYhO0Qahfehtj9jG8_TgACPAQAAniSOUftryz9u6Af_jYE',
        'documento2': 'BQACAgEAAxkBAAI4oGdmtA4p7qsi_pCdranI8h4aT_O9AAL1BAACJn44RxBiRRjteVm6NgQ',
        'documento3': 'BQACAgEAAxkBAAI4oWdmtA5qJ9fhwy8nDerq70sYUfHIAAI9BAACeJI5R1k_-h61nkMAATYE',
        'perfil_mobile': 'AgACAgEAAxkBAAJI5WfpffsHwNx_i3waE3tg9UxaJ64MAAJtrTEbGpNJR7nlMy_PL0kmAQADAgADeQADNgQ',
        'recorte_png': 'BAACAgEAAxkBAAI_7mfEuFXdCANx7nMNdmmrP-_MQ9kDAAIdBAACi5sgRhE48Cw8pjxoNgQ',
        'imagens_detalhadas': {
            'col_img_1': {'nome_botao': '📷 Imagem #1', 'file_id': 'PLACEHOLDER_COL_IMG1'},
        },
        'carrosseis': {
            'col_car_1': {'nome_botao': '🎠 Carrossel #1', 'file_ids': ['PLACEHOLDER_COL_C1_IMG1']},
        }
     },
    'beneficioglutamineprime': {
        'video': 'BAACAgEAAxkBAAIWjmcIfIMTskdTF3V_KmOotze7gqdeAALOBAACynwwRARdX5BQ54SPNgQ',
        'documento': 'BQACAgEAAxkBAAIWkGcIfS4NVmA9kOU0cj7Fj6LKdv50AAICBQACTQpBRG2aA-lUC6N-NgQ',
        'perfil_mobile': 'AgACAgEAAxkBAAJI6mfpfjRVQDz12l9jfEeLTv9TOusaAAJvrTEbGpNJR56RpgVLJFPpAQADAgADeQADNgQ',
        'recorte_png': 'BAACAgEAAxkBAAI_6GfEt21AYAZY9p6RKH1sPMgwQ7jbAAIaBAACi5sgRnbRXrWzyOXANgQ',
        'imagens_detalhadas': {
            'glu_img_1': {'nome_botao': '📷 Imagem #1', 'file_id': 'PLACEHOLDER_GLU_IMG1'},
        },
        'carrosseis': {
            'glu_car_1': {'nome_botao': '🎠 Carrossel #1', 'file_ids': ['PLACEHOLDER_GLU_C1_IMG1']},
        }
    },
    'beneficiotfmastigavel': {
        'video': 'BAACAgEAAxkBAAI4zmdocXrHaVWPQP1cwblA1ANMPu7wAAJCBgACgvBIRw2goJ75LdDkNgQ',
        'perfil_mobile': 'AgACAgEAAxkBAAJI7mfpfm_opqE5aP3S9lrBVLKwsKp3AAJwrTEbGpNJR11OgLJD2wPAAQADAgADeQADNgQ',
        'documento': 'BQACAgEAAxkBAAI45WdoeZ-bTPJUtsn1s8RVUSLNkpv1AAIYBAAC80lIRxRRAwAB5DCZhjYE',
        'recorte_png': 'BAACAgEAAxkBAAI_9mfEucTCAqMPZlsWSPZpvO8hE_PmAAIhBAACi5sgRiq5PAX4c5ErNgQ',
        'imagens_detalhadas': {
            'tfm_img_1': {'nome_botao': '📷 Imagem #1', 'file_id': 'PLACEHOLDER_TFM_IMG1'},
        },
        'carrosseis': {
            'tfm_car_1': {'nome_botao': '🎠 Carrossel #1', 'file_ids': ['PLACEHOLDER_TFM_C1_IMG1']},
        }
    },
}

PITCH_DE_VENDA_TEXT = {
    'beneficioriovidaburst': """🫐 *RioVida Burst 4Life*: Saúde e sabor! 💥

Sinta o poder dos antioxidantes e Transfer Factors em cada sachê, apoiando seu corpo e aumentando sua energia:

1️⃣ *Imunidade Reforçada:* Aumente a sua resistência, promovendo mais saúde.
2️⃣ *Energia Sem Limites:* Diga adeus ao cansaço, aproveitando cada momento com mais disposição.
3️⃣ *Proteção Antioxidante:* Neutralize os radicais livres, mantendo a sua pele com aparência jovem.
4️⃣ *Bem-Estar Completo:* Melhore o seu humor, fortaleça o seu corpo e sinta-se no auge da sua forma física e mental.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), açaí, blueberry, sabugueiro, uva e romã.

*Modo de tomar:* Consuma um sachê ao dia.

*RioVida Burst*: A sua dose diária de saúde e energia! 🫐
""",
    'beneficioriovidastix': """🍷🍇 *RioVida Stix 4Life*: Refrescância e imunidade! 🍷

Transforme a sua água em uma aliada da sua saúde com esta combinação de Transfer Factor e antioxidantes:

1️⃣ *Defesa Imunológica:* Fortaleça o seu sistema imunológico.
2️⃣ *Hidratação Turbinada:* Refresque-se com o sabor de frutas vermelhas.
3️⃣ *Praticidade Imbatível:* Leve os seus sticks para onde quiser.
4️⃣ *Proteção Celular:* Neutralize os radicais livres e promova o bem estar.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), vitamina C, extrato de romã, açaí e blueberry.

*Modo de tomar:* Misture um stick em 500ml de água. Consuma uma vez ao dia.

*RioVida Stix*: A maneira mais prática de cuidar da sua saúde! 🍷🍇
""",
    'beneficiobioefa': """🌿 *BioEFA 4Life*: Um corpo em equilíbrio! 🌿

Nutra o seu organismo com os ácidos graxos essenciais que ele precisa para funcionar:

1️⃣ *Coração Saudável:* Cuide da sua saúde cardiovascular.
2️⃣ *Cérebro Ativo:* Melhore a sua memória e concentração.
3️⃣ *Imunidade Fortalecida:* Equilibre a resposta inflamatória.
4️⃣ *Pele Radiante:* Hidrate e proteja a sua pele.

*Ingredientes Principais:* Óleo de peixe, óleo de linhaça e óleo de borragem.

*Modo de tomar:* Tome duas (2) cápsulas softgel ao dia, com 240ml de líquido.

*BioEFA*: Uma vida mais longa e saudável! 🌿
""",
    'beneficioenergygostix': """⚡ *Energy Go Stix 4Life*: Energia e foco! ⚡

Transforme o seu dia com esta explosão de sabor e vitalidade, que te ajuda a superar o cansaço:

1️⃣ *Energia Instantânea:* Sinta um impulso imediato de energia.
2️⃣ *Foco Implacável:* Aumente a sua concentração e clareza mental.
3️⃣ *Proteção Antioxidante:* Defenda as suas células contra os radicais livres.
4️⃣ *Praticidade Absoluta:* Leve os seus sticks para onde quiser.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), chá verde, guaraná, vitaminas do complexo B.

*Modo de tomar:* Dissolva um stick em 240ml de água. Consuma uma vez ao dia.

*Energy Go Stix*: Um dia produtivo e cheio de energia! ⚡
""",
    'beneficiotfplus': """🐣🐄🍄🔝 *TF Plus 4Life*: A proteção imunológica! 🛡️

Dê ao seu sistema imunológico o suporte que ele precisa:

1️⃣ *Imunidade Potencializada:* Aumente a atividade das suas células de defesa.
2️⃣ *Bem-Estar Integral:* Sinta mais disposição e qualidade de vida.
3️⃣ *Proteção Celular Avançada:* Defenda as suas células contra os danos.
4️⃣ *Ingredientes Premium:* Desfrute de uma fórmula com ingredientes naturais.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), cogumelos maitake e shiitake, zinco, vitamina C.

*Modo de tomar:* Tome duas (2) cápsulas ao dia, com 240ml de líquido.

*TF Plus*: Uma vida mais saudável! 🛡️
""",
    'beneficiotfplus30caps': """💊 *TF Plus 30 Cápsulas 4Life*: Seu Reforço Imunológico Concentrado e Prático! ✨

A potência máxima do TF Plus, agora na conveniência de uma embalagem com 30 cápsulas. Ideal para quem busca experimentar os benefícios incríveis dos Fatores de Transferência ou precisa de uma solução compacta para manter a imunidade blindada em qualquer lugar.

1️⃣ *Imunidade Inteligente:* Fórmula avançada com Fatores de Transferência e o exclusivo blend Cordyvant™ para educar, fortalecer e equilibrar seu sistema de defesa.
2️⃣ *Praticidade Total:* Leve com você para viagens, trabalho ou para o dia a dia, garantindo sua dose de proteção.
3️⃣ *Resultados Comprovados:* Baseado na ciência dos Fatores de Transferência, que há décadas ajudam a promover saúde e bem-estar.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), blend Cordyvant™ (incluindo cogumelos maitake, shiitake, cordyceps, beta-glucanos e mais), Zinco.

*Modo de tomar:* Tome uma (1) cápsula ao dia com 240ml de líquido, ou conforme orientação profissional.

*TF Plus 30 Cápsulas*: A escolha inteligente para uma imunidade de ferro! 💪🛡️
""",
    'beneficiotfzinco': """🐣🐄 *TF Zinco 4Life*: Imunidade! 💪

Fortaleça o seu sistema imunológico com a combinação de Transfer Factor e Zinco:

1️⃣ *Defesas Blindadas:* Aumente a sua resistência.
2️⃣ *Pele Radiante:* Cuide da saúde da sua pele.
3️⃣ *Ação Antioxidante:* Proteja as suas células contra os radicais livres.
4️⃣ *Suporte Nutricional Essencial:* Garanta o aporte de Zinco.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), Zinco.

*Modo de tomar:* Tome um (1) tablete ao dia, com 240ml de líquido.

*TF Zinco*: Imunidade e bem-estar! 💪
""",
    'beneficionutrastart': """🥤🍽️ *NutraStart 4Life*: O café da manhã ideal! ☀️

Comece o seu dia com energia, vitalidade e todos os nutrientes que você precisa:

1️⃣ *Nutrição Completa:* Desfrute de um shake equilibrado, rico em proteínas, fibras, vitaminas e minerais.
2️⃣ *Imunidade Fortalecida:* Reforce o seu sistema imunológico.
3️⃣ *Controle de Peso Inteligente:* Alcance os seus objetivos.
4️⃣ *Praticidade Sem Igual:* Prepare o seu shake em segundos.

*Ingredientes Principais:* Proteína de soro do leite, fibra de aveia, 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), vitaminas e minerais.

*Modo de tomar:* Misture um scoop em 240ml de água ou leite. Consuma no café da manhã ou como substituto de refeição.

*NutraStart*: Um dia produtivo e cheio de energia! ☀️
""",
    'beneficioprotf': """🏋️‍♂️💪 *PRO-TF 4Life*: A proteína que redefine os seus limites! 🚀

Alcance resultados com esta fórmula para te ajudar a construir músculos e elevar o seu desempenho:

1️⃣ *Músculos Poderosos:* Estimule a síntese proteica e maximize o ganho de massa muscular.
2️⃣ *Queima de Gordura Acelerada:* Turbine o seu metabolismo.
3️⃣ *Desempenho Imbatível:* Aumente a sua força e resistência.
4️⃣ *Imunidade Blindada:* Fortaleça o seu sistema imunológico.

*Ingredientes Principais:* Proteína do soro do leite hidrolisada, proteína do ovo hidrolisada, 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo).

*Modo de tomar:* Misture um scoop em 240ml de água ou sua bebida preferida após o treino ou quando precisar de um aporte proteico.

*PRO-TF*: Uma saúde inabalável! 🚀
""",
    'beneficiocolageno': """💧🌟 *Transfer Factor Collagen da 4Life*: A beleza e bem-estar em um só suplemento! ✨

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
    'beneficiotfboost': """🍊✴️ *TF Boost 4Life*: Desperte a sua energia interior! 🌟

Revitalize o seu corpo e mente com esta fórmula, que combina Transfer Factor, antioxidantes e ingredientes energizantes:

1️⃣ *Energia Infinita:* Sinta energia, mantendo você ativo.
2️⃣ *Foco Laser:* Melhore a sua concentração e clareza mental.
3️⃣ *Proteção Antioxidante Avançada:* Defenda as suas células contra os radicais livres.
4️⃣ *Suporte Imunológico Completo:* Reforce o seu sistema imunológico.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), guaraná, chá verde, vitamina C, acerola.

*Modo de tomar:* Dissolva um sachê em 240ml de água. Consuma uma vez ao dia.

*TF Boost*: Vitalidade! 🌟
""",
    'beneficioglutamineprime': """⛽⚡🔬 *4Life NanoFactor Glutamine Prime* é o segredo para um sistema imunológico forte! 😎

A glutamina é um aminoácido essencial para a saúde das suas células de defesa. Descubra como este suplemento pode otimizar sua imunidade:

✨ *Combustível para a Imunidade:* Fornece energia para as células do sistema imunológico, aumentando sua capacidade de combater agressores.
✨ *Reparação e Crescimento:* Auxilia na síntese de DNA e proteínas, importantes para a manutenção celular e recuperação.
✨ *Proteção Integral:* Fortalece as barreiras do seu corpo, auxiliando a manter a integridade celular.

*Ingredientes Principais:* Glutamina, NanoFactor® (concentrado de ultrafiltração de proteínas do soro do leite de vaca e gema de ovo de galinha).

*Modo de tomar:* Misture um sachê em 240ml de água ou sua bebida preferida. Consuma uma vez ao dia.

Invista em *4Life NanoFactor Glutamine Prime* e sinta a diferença!
""",
    'beneficiotfmastigavel': """🍊🟠 *TF Mastigável 4Life*: Imunidade com sabor! 😄

Proteja a saúde dos seus filhos com estes tabletes mastigáveis que combinam Transfer Factor:

1️⃣ *Defesas Fortificadas:* Aumente a resistência.
2️⃣ *Sabor Irresistível:* Transforme a suplementação em um momento prazeroso.
3️⃣ *Praticidade Para o Dia a Dia:* Leve os tabletes para onde quiser.
4️⃣ *Saúde Para Toda a Família:* Cuide da imunidade de todos.

*Ingredientes Principais:* 4Life Transfer Factor Tri-Factor Formula (colostro bovino e gema de ovo), vitamina C, acerola.

*Modo de tomar:* Mastigue dois (2) tabletes ao dia. Para crianças menores, esmague o tablete e misture com a comida.

*TF Mastigável*: Proteção! 😄
"""
}

