import streamlit as st
import base64
import os
from pathlib import Path

# --- HELPER FUNCTIONS ---

def audio_to_base64(file_path):
    """Convert audio file to base64 for embedding"""
    try:
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.warning(f"Audio file not found: {file_path}")
        return None

def play_audio_with_user_interaction(file_path, audio_id=None):
    """Play audio that requires user interaction (mobile-friendly)"""
    audio_b64 = audio_to_base64(file_path)
    if not audio_b64:
        return
    
    if not audio_id:
        import random
        audio_id = f"audio-{random.randint(0,9999999)}"
    
    st.markdown(
        f"""
        <audio id="{audio_id}" preload="auto">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
        <script>
        setTimeout(function() {{
            var audio = document.getElementById('{audio_id}');
            if (audio) {{
                audio.play().catch(function(error) {{
                    console.log('Audio play failed:', error);
                }});
            }}
        }}, 100);
        </script>
        """, 
        unsafe_allow_html=True
    )

def play_background_music():
    """Play background music with lower volume"""
    audio_b64 = audio_to_base64("sounds/decision.mp3")
    if not audio_b64:
        return
        
    st.markdown(
        f"""
        <audio id="bg-music" preload="auto" loop>
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
        <script>
        setTimeout(function() {{
            var bgm = document.getElementById('bg-music');
            if (bgm) {{
                bgm.volume = 0.3;
                bgm.play().catch(function(error) {{
                    console.log('Background music play failed:', error);
                }});
            }}
        }}, 200);
        </script>
        """, 
        unsafe_allow_html=True
    )

def get_valid_path(img_path):
    """Get valid image path"""
    local = Path(img_path)
    if local.exists():
        return img_path
    nested = Path(f"oyun/{img_path}")
    if nested.exists():
        return str(nested)
    return img_path

def image_to_base64(img_path):
    """Convert image to base64 for HTML embedding"""
    try:
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.warning(f"Image file not found: {img_path}")
        return None

# --- MOBILE-OPTIMIZED CSS ---
css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&display=swap');

* {
    box-sizing: border-box;
}

body {
    background: linear-gradient(135deg, #8B4513 0%, #D2691E 50%, #CD853F 100%);
    color: #2F1B14;
    font-family: 'Cinzel', serif;
    margin: 0;
    padding: 0;
}

.main-container {
    max-width: 100vw;
    padding: 10px;
    min-height: 100vh;
}

.game-header {
    text-align: center;
    background: linear-gradient(145deg, #F4E4BC, #E6D3A3);
    border: 3px solid #8B4513;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.game-title {
    font-size: clamp(24px, 6vw, 36px);
    font-weight: 700;
    color: #8B4513;
    margin: 0;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}

.parchment {
    background: linear-gradient(145deg, #F5E6D3, #E8D5B7);
    margin: 15px 0;
    padding: 20px;
    border: 2px solid #8B4513;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    line-height: 1.6;
}

.character-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 15px;
    padding: 20px 0;
    justify-items: center;
}

.character-card {
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 15px;
    border-radius: 15px;
    background: rgba(245, 230, 211, 0.8);
    border: 3px solid transparent;
    width: 100%;
    max-width: 150px;
}

.character-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0,0,0,0.3);
}

.character-card.selected {
    border-color: #228B22;
    background: rgba(34, 139, 34, 0.1);
    transform: translateY(-3px);
}

.char-img {
    width: 100%;
    height: auto;
    max-width: 100px;
    border-radius: 50%;
    border: 4px solid #8B4513;
    margin-bottom: 10px;
    transition: border-color 0.3s ease;
}

.character-card.selected .char-img {
    border-color: #228B22;
}

.char-name {
    font-size: 16px;
    font-weight: 600;
    color: #8B4513;
    margin: 0;
}

.score-display {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 20px;
}

.score-item {
    background: linear-gradient(145deg, #FFD700, #FFA500);
    padding: 10px 15px;
    border-radius: 20px;
    border: 2px solid #8B4513;
    font-weight: 600;
    font-size: 14px;
    text-align: center;
    min-width: 80px;
}

.game-button {
    background: linear-gradient(145deg, #228B22, #32CD32);
    color: white;
    border: none;
    padding: 15px 30px;
    border-radius: 25px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    max-width: 300px;
    margin: 10px auto;
    display: block;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.game-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.3);
}

.game-button:disabled {
    background: #cccccc;
    cursor: not-allowed;
    transform: none;
}

.options-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 20px 0;
}

.option-button {
    background: linear-gradient(145deg, #F5E6D3, #E8D5B7);
    border: 2px solid #8B4513;
    padding: 15px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: left;
    font-size: 14px;
    line-height: 1.4;
}

.option-button:hover {
    background: linear-gradient(145deg, #E8D5B7, #DBC4A2);
    transform: translateX(5px);
}

.option-button.selected {
    background: linear-gradient(145deg, #98FB98, #90EE90);
    border-color: #228B22;
}

.reset-button {
    background: linear-gradient(145deg, #DC143C, #FF6347);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    font-size: 14px;
    cursor: pointer;
    margin-top: 20px;
    transition: all 0.3s ease;
}

.loading-screen {
    text-align: center;
    padding: 50px 20px;
}

.loading-text {
    font-size: 24px;
    color: #8B4513;
    margin-bottom: 20px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

@media (max-width: 768px) {
    .character-grid {
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
    }
    
    .score-display {
        flex-direction: column;
        align-items: center;
    }
    
    .score-item {
        width: 100%;
        max-width: 200px;
    }
}

/* Hide Streamlit elements for cleaner mobile experience */
.stDeployButton {display:none;}
footer {visibility: hidden;}
.stDecoration {display:none;}
header {visibility: hidden;}
</style>
"""

st.markdown(css, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "current_screen" not in st.session_state:
    st.session_state.current_screen = "character_select"

if "selected_character" not in st.session_state:
    st.session_state.selected_character = None

if "character_confirmed" not in st.session_state:
    st.session_state.character_confirmed = False

if "audio_played" not in st.session_state:
    st.session_state.audio_played = {"character": False, "start": False, "background": False}

if "game_data" not in st.session_state:
    st.session_state.game_data = {
        "current_scene": "bolum_1",
        "history": [],
        "scores": {"harem": 0, "suleyman": 0, "divan": 0}
    }

if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

# --- GAME SCENARIOS ---
scenarios = {
            # İlk 50 bölüm (örnek)
            "bolum_1": {
                "description": "Hürrem, Manisa'dan gelen tüccarların uğradığı usulsüzlükleri duydu. Sarayda bu konu büyük bir mesele haline geldi.",
                "options": {
                    "A": {
                        "text": "Sessiz kal ve olaya karışma.",
                        "outcome": "Hürrem olaylara karışmadı ve güvenli bir konumda kaldı. Ancak etkisini artırma şansını kaçırdı.",
                        "score_changes": {"harem": 0, "suleyman": -1, "divan": 0},
                        "next_scene": "bolum_2"
                    },
                    "B": {
                        "text": "Usulsüzlükleri açıkça eleştir.",
                        "outcome": "Hürrem, cesaretini göstererek dikkatleri üzerine çekti. Ancak bazı güçlü kişiler düşman oldu.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": -2},
                        "next_scene": "bolum_2"
                    },
                    "C": {
                        "text": "Usulsüzlükleri dolaylı şekilde ima et.",
                        "outcome": "Hürrem, zekice davranarak dikkat çekmeden konumunu güçlendirdi.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_2"
                    }
                }
            },
            "bolum_2": {
                "description": "Hürrem, güzelliği ve terbiyeli davranışlarıyla Valide Sultan ile karşılaşır. Bu durum, onun sarayda nasıl konumlanacağına dair kritik ipuçları verir.",
                "options": {
                    "A": {
                        "text": "Valide Sultan'a uyum sağla.",
                        "outcome": "Hürrem, Valide Sultan'ın güvenini kazandı ama kişisel özgürlüğünden ödün verdi.",
                        "score_changes": {"harem": 2, "suleyman": -1, "divan": 0},
                        "next_scene": "bolum_3"
                    },
                    "B": {
                        "text": "Zekanı ve yeteneklerini göster.",
                        "outcome": "Hürrem, zekasını sergileyerek dikkat çekti fakat Valide Sultan’ın hoşuna gitmedi.",
                        "score_changes": {"harem": -1, "suleyman": 2, "divan": 0},
                        "next_scene": "bolum_3"
                    },
                    "C": {
                        "text": "Hem terbiyeli hem zeki bir profil çiz.",
                        "outcome": "Hürrem, dengeli bir strateji ile saygınlığını artırdı.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_3"
                    }
                }
            },
            "bolum_3": {
                "description": "Hürrem, saraydaki konumunu sağlamlaştırmak için diplomatik bir adım atar ve yeni ittifaklar kurma fırsatı yakalar.",
                "options": {
                    "A": {
                        "text": "Valide Sultan ile ittifak yap.",
                        "outcome": "Hürrem, Valide Sultan ile güçlü bir ittifak kurdu.",
                        "score_changes": {"harem": 3, "suleyman": -1, "divan": 0},
                        "next_scene": "bolum_4"
                    },
                    "B": {
                        "text": "İbrahim Paşa'yı kendi tarafına çek.",
                        "outcome": "Hürrem, İbrahim Paşa ile geçici bir anlaşmaya vardı ve sarayda önemli adımlar attı.",
                        "score_changes": {"harem": 0, "suleyman": 1, "divan": 2},
                        "next_scene": "bolum_4"
                    },
                    "C": {
                        "text": "Bağımsız hareket et.",
                        "outcome": "Hürrem, kendi planlarını uygulamaya başladı, fakat bu durum riskleri de beraberinde getirdi.",
                        "score_changes": {"harem": -2, "suleyman": 0, "divan": -1},
                        "next_scene": "bolum_4"
                    }
                }
            },
            "bolum_4": {
                "description": "Saraydaki rakipler güç kazanırken, Hürrem stratejik bir karar verme zamanıyla karşı karşıya.",
                "options": {
                    "A": {
                        "text": "Rakiplerini etkisiz hale getir.",
                        "outcome": "Hürrem, rakiplerini zekice hamlelerle etkisiz hale getirdi.",
                        "score_changes": {"harem": 2, "suleyman": 2, "divan": -1},
                        "next_scene": "bolum_5"
                    },
                    "B": {
                        "text": "İttifaklar kurarak dengeleri koru.",
                        "outcome": "Hürrem, güçlü ittifaklar kurarak saraydaki konumunu güçlendirdi.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_5"
                    },
                    "C": {
                        "text": "Güçlü rakiplere karşı tarafsız kal.",
                        "outcome": "Hürrem tarafsız kaldı ancak önemli fırsatları kaçırdı.",
                        "score_changes": {"harem": -1, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_5"
                    }
                }
            },
            "bolum_5": {
                "description": "Hürrem, saraydaki konumunu güçlendirmek için stratejik hamleler yapar. Yeni rakipler ve siyasi belirsizlik ortada.",
                "options": {
                    "A": {
                        "text": "Gizli operasyonlar başlat.",
                        "outcome": "Hürrem, rakiplerinin sırlarına ulaşmak için gizli operasyonlar başlattı.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_6"
                    },
                    "B": {
                        "text": "Açık meydan okuma yap.",
                        "outcome": "Açık meydan okuma riskliydi, ancak bazı destekçiler kazandı.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": -1},
                        "next_scene": "bolum_6"
                    },
                    "C": {
                        "text": "Tarafsız kalarak durumu gözlemle.",
                        "outcome": "Gözlem, stratejik kararlar almak için değerli bilgiler sağladı.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_6"
                    }
                }
            },
            "bolum_6": {
                "description": "Hürrem, saray entrikalarını yakından izlemeye başlar ve gizli ittifaklar kurmanın yollarını araştırır.",
                "options": {
                    "A": {
                        "text": "Sessizce gözlemle ve bilgi topla.",
                        "outcome": "Sessiz gözlemlerle rakiplerinin zayıf noktalarını öğrendi.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_7"
                    },
                    "B": {
                        "text": "Açıkça sesini yükselt ve adaletsizlikleri dile getir.",
                        "outcome": "Cesur davranışıyla dikkat çekti, ancak düşmanlar edindi.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": -1},
                        "next_scene": "bolum_7"
                    },
                    "C": {
                        "text": "Arka planda hareket et, rakipleri manipüle et.",
                        "outcome": "Rakiplerini kendi çıkarları doğrultusunda yönlendirmeyi başardı.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_7"
                    }
                }
            },
            "bolum_7": {
                "description": "Sarayda politik gerilim artıyor. Hürrem, güç dengelerini gözlemliyor ve yeni ittifaklar kurma fırsatlarını değerlendiriyor.",
                "options": {
                    "A": {
                        "text": "Sessizce ittifaklar kur.",
                        "outcome": "Gizli ittifaklar kurarak gelecekteki hamleler için zemin hazırladı.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_8"
                    },
                    "B": {
                        "text": "Açık meydan okuma yap.",
                        "outcome": "Açık meydan okuma riskliydi, ancak bazı destekçiler kazandı.",
                        "score_changes": {"harem": 0, "suleyman": 2, "divan": -1},
                        "next_scene": "bolum_8"
                    },
                    "C": {
                        "text": "Durumu analiz et, strateji geliştir.",
                        "outcome": "Analitik yaklaşım ona uzun vadede avantaj sağladı.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_8"
                    }
                }
            },
            "bolum_8": {
                "description": "Hürrem, devlet işlerine dair önemli diplomatik fırsatlarla karşı karşıya. Yabancı elçiler ve devlet adamlarıyla temaslar artıyor.",
                "options": {
                    "A": {
                        "text": "Valide Sultan ile samimi bir ilişki kur.",
                        "outcome": "Valide Sultan’ın desteğini kazandı, ancak kişisel bağımsızlığından ödün verdi.",
                        "score_changes": {"harem": 2, "suleyman": -1, "divan": 0},
                        "next_scene": "bolum_9"
                    },
                    "B": {
                        "text": "İbrahim Paşa ile yakınlaş, gizli ittifak yap.",
                        "outcome": "İbrahim Paşa ile ittifak yaparak sarayda önemli adımlar attı.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 2},
                        "next_scene": "bolum_9"
                    },
                    "C": {
                        "text": "Kendi stratejinizi uygulayın.",
                        "outcome": "Kendi planlarınıza sadık kaldınız, fakat yalnızlık ve risk ortaya çıktı.",
                        "score_changes": {"harem": -2, "suleyman": 0, "divan": -1},
                        "next_scene": "bolum_9"
                    }
                }
            },
            "bolum_9": {
                "description": "Sarayda Hürrem, rakipleri tarafından kıskanılmaya başlar. Güç dengeleri sarsılırken stratejik hamleler kaçınılmaz hale gelir.",
                "options": {
                    "A": {
                        "text": "Düşmanlara karşı sert önlemler al.",
                        "outcome": "Sert hamlelerle rakiplerinize zarar verdiniz, ancak bazıları öfkeyle karşılık verdi.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": -2},
                        "next_scene": "bolum_10"
                    },
                    "B": {
                        "text": "Diplomatik yollarla dengeyi koruyun.",
                        "outcome": "Diplomatik hamlelerle ortamı stabilize etmeye çalıştınız.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_10"
                    },
                    "C": {
                        "text": "Tarafsız kalarak durumu gözlemleyin.",
                        "outcome": "Tarafsızlık kısa vadede faydalı oldu ancak önemli fırsatları kaçırdınız.",
                        "score_changes": {"harem": -1, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_10"
                    }
                }
            },
            "bolum_10": {
                "description": "Sarayda devlet işlerinde yeni gelişmeler yaşanıyor. Hürrem, artan düşmanlık ve siyasi belirsizlikle başa çıkmaya çalışıyor.",
                "options": {
                    "A": {
                        "text": "Devlete bağlılığınızı vurgulayın.",
                        "outcome": "Devlete olan bağlılığınızı gösterip destek kazandınız.",
                        "score_changes": {"harem": 1, "suleyman": 2, "divan": 0},
                        "next_scene": "bolum_11"
                    },
                    "B": {
                        "text": "Kendi çıkarlarınızı ön plana çıkarın.",
                        "outcome": "Kendi çıkarlarınıza odaklanarak riskli hamleler yaptınız.",
                        "score_changes": {"harem": -1, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_11"
                    },
                    "C": {
                        "text": "Dengede kalmaya çalışın.",
                        "outcome": "Dengeli yaklaşım kısa vadede istikrar sağladı.",
                        "score_changes": {"harem": 0, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_11"
                    }
                }
            },
            "bolum_11": {
                "description": "Hürrem, saraydaki güç dengelerini ve entrikaları derinlemesine analiz ediyor. Gizli casusluk faaliyetlerine başlaması kritik önem taşıyor.",
                "options": {
                    "A": {
                        "text": "Gizli casusluk faaliyetlerine başla.",
                        "outcome": "Casusluk sayesinde rakiplerinizin zayıf noktalarını öğrendiniz.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_12"
                    },
                    "B": {
                        "text": "Rakiplerinize karşı açık mücadeleye girin.",
                        "outcome": "Açık mücadele, rakiplerinizi geçici olarak zayıflattı fakat riskler arttı.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": -1},
                        "next_scene": "bolum_12"
                    },
                    "C": {
                        "text": "Tarafsız kalarak durumu gözlemleyin.",
                        "outcome": "Gözlem yaparak stratejik veriler topladınız, ancak hamleye geçemediniz.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_12"
                    }
                }
            },
            "bolum_12": {
                "description": "Hürrem, sarayda yeni ittifaklar kuruluyor. Rakipleri ve potansiyel müttefikleri değerlendirip stratejinizi oluşturun.",
                "options": {
                    "A": {
                        "text": "Güçlü müttefiklerle ittifak kurun.",
                        "outcome": "Sağlam ittifaklar sayesinde konumunuzu güçlendirdiniz.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_13"
                    },
                    "B": {
                        "text": "Rakiplerinize karşı saldırgan davranın.",
                        "outcome": "Açık saldırı, rakiplerinizi zayıflattı fakat riskler arttı.",
                        "score_changes": {"harem": 1, "suleyman": 2, "divan": -1},
                        "next_scene": "bolum_13"
                    },
                    "C": {
                        "text": "Orta yolu seçip dengede kalın.",
                        "outcome": "Dengeli yaklaşım uzun vadede istikrar sağladı.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_13"
                    }
                }
            },
             "bolum_13": {
          "description": "Hürrem, rakiplerinden gelen baskılarla yüzleşmek zorunda. Siyasi ve ailevi entrikalar derinleşiyor.",
          "options": {
            "A": {
              "text": "Açıkça meydan oku.",
              "outcome": "Meydana okuma, düşmanlarını harekete geçirdi.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": -2 },
              "next_scene": "bolum_14"
            },
            "B": {
              "text": "Gizli operasyonlara devam et.",
              "outcome": "Gizli hamleler, rakiplerini şaşırttı ve avantaj sağladı.",
              "score_changes": { "harem": 1, "suleyman": 0, "divan": 1 },
              "next_scene": "bolum_14"
            },
            "C": {
              "text": "Diplomatik yolları seç.",
              "outcome": "Diplomasi, bazı sorunları hafifletti ancak net bir üstünlük sağlamadı.",
              "score_changes": { "harem": 0, "suleyman": 1, "divan": 0 },
              "next_scene": "bolum_14"
            }
          }
        },

        "bolum_14": {
          "description": "Saraydaki entrikalar derinleşiyor. Hürrem, aile meseleleri ve devlet işleri arasında kritik kararlar almak zorunda.",
          "options": {
            "A": {
              "text": "Aile ilişkilerinde baskın davran.",
              "outcome": "Aile içindeki gücünü artırdı, fakat sarayda düşmanlık yarattı.",
              "score_changes": { "harem": 2, "suleyman": -1, "divan": 0 },
              "next_scene": "bolum_15"
            },
            "B": {
              "text": "Devlet işlerine odaklan.",
              "outcome": "Devlet meselelerinde başarılı adımlar attı, ancak aile desteğinde eksiklikler oluştu.",
              "score_changes": { "harem": 1, "suleyman": 2, "divan": 0 },
              "next_scene": "bolum_15"
            },
            "C": {
              "text": "Her iki alanda dengede kal.",
              "outcome": "Dengeli yaklaşım, uzun vadeli istikrar sağladı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_15"
            }
          }
        },
        "bolum_15": {
          "description": "Hürrem, yeni rakiplerle karşı karşıya. Siyasi ve ailevi engeller artarken, stratejik hamleler kaçınılmaz hale geliyor.",
          "options": {
            "A": {
              "text": "Açık rekabet et.",
              "outcome": "Rekabetçi tavrıyla dikkat çekti, fakat riskler de arttı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": -1 },
              "next_scene": "bolum_16"
            },
            "B": {
              "text": "Gizli ittifaklar kur.",
              "outcome": "Gizli ittifaklar, rakiplerini zayıflatmasına yardımcı oldu.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_16"
            },
            "C": {
              "text": "İşbirliği yap.",
              "outcome": "Ortak hareket etmek, beklenmedik destekler getirdi.",
              "score_changes": { "harem": 0, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_16"
            }
          }
        },
        "bolum_16": {
          "description": "Saray entrikaları yoğunlaşıyor. Hürrem, düşmanlarıyla yüzleşirken içsel çatışmalar yaşıyor.",
          "options": {
            "A": {
              "text": "Düşmanlarına karşı acımasız ol.",
              "outcome": "Acımasız hamleler, düşmanlarını dehşete düşürdü.",
              "score_changes": { "harem": 2, "suleyman": 2, "divan": -2 },
              "next_scene": "bolum_17"
            },
            "B": {
              "text": "İçsel çatışmalarını bastır ve strateji geliştir.",
              "outcome": "Duygularını kontrol altında tutarak stratejik hamleler yaptı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_17"
            },
            "C": {
              "text": "Tarafsız kalarak durumu gözlemle.",
              "outcome": "Tarafsızlık, kısa vadede riskleri azaltırken uzun vadede fırsatları kaçırdı.",
              "score_changes": { "harem": 0, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_17"
            }
          }
        },
        "bolum_17": {
          "description": "Devlet işleri karmaşıklaşıyor. Hürrem, yeni fırsatlar ve tehlikeler arasında kritik bir seçim yapmalı.",
          "options": {
            "A": {
              "text": "Diplomatik girişimlerde bulun.",
              "outcome": "Diplomatik hamleler, bazı sorunları yumuşattı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_18"
            },
            "B": {
              "text": "Rakiplerine karşı agresif ol.",
              "outcome": "Agresif tavrı, rakiplerini korkuttu ama düşman çevresini genişletti.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": -1 },
              "next_scene": "bolum_18"
            },
            "C": {
              "text": "Gizli stratejiler geliştir.",
              "outcome": "Gizli planlar, uzun vadede beklenmedik avantajlar sağladı.",
              "score_changes": { "harem": 1, "suleyman": 0, "divan": 1 },
              "next_scene": "bolum_18"
            }
          }
        },
        "bolum_18": {
          "description": "Hürrem, aile içindeki ve devlet içindeki rekabetle yüzleşiyor. Kendi çocuklarının geleceği tehlikede.",
          "options": {
            "A": {
              "text": "Çocuklarını destekle ve güçlendir.",
              "outcome": "Eğitim ve destek, çocuklarının geleceğini güvence altına aldı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_19"
            },
            "B": {
              "text": "Rakip çocuklara karşı agresif davran.",
              "outcome": "Agresif tavır, rakiplerini zayıflattı ancak aile içi gerilimi artırdı.",
              "score_changes": { "harem": 1, "suleyman": 2, "divan": -1 },
              "next_scene": "bolum_19"
            },
            "C": {
              "text": "Tarafsız kalarak durumu gözlemle.",
              "outcome": "Tarafsızlık kısa vadede denge sağladı, ancak risk oluşturdu.",
              "score_changes": { "harem": 0, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_19"
            }
          }
        },
        "bolum_19": {
          "description": "Sarayda yeni düzenlemeler ve güç mücadeleleri baş gösteriyor. Hürrem, devletin geleceğini sorguluyor.",
          "options": {
            "A": {
              "text": "Devlete bağlılığını vurgula.",
              "outcome": "Devlete olan bağlılığını açıkça gösterdi ve destek kazandı.",
              "score_changes": { "harem": 1, "suleyman": 2, "divan": 0 },
              "next_scene": "bolum_20"
            },
            "B": {
              "text": "Kendi çıkarlarını ön plana çıkar.",
              "outcome": "Kendi çıkarlarına odaklanması, bazı çevrelerde hoş karşılanmadı.",
              "score_changes": { "harem": -1, "suleyman": 0, "divan": 1 },
              "next_scene": "bolum_20"
            },
            "C": {
              "text": "Dengede kalmaya çalış.",
              "outcome": "Dengeli yaklaşım, kısa vadede istikrar sağladı.",
              "score_changes": { "harem": 0, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_20"
            }
          }
        },
        "bolum_20": {
          "description": "Saraydaki entrikalar daha da yoğunlaşıyor. Hürrem, devlet işleri ve aile ilişkileri arasında ikilem yaşıyor.",
          "options": {
            "A": {
              "text": "Süleyman'ın seferini coşkuyla destekle.",
              "outcome": "Süleyman'ın yanında olduğunu belli etti, böylece destek kazandı.",
              "score_changes": { "harem": 1, "suleyman": 2, "divan": 0 },
              "next_scene": "bolum_21"
            },
            "B": {
              "text": "Sarayda güç mücadelesine giriş yap.",
              "outcome": "Güç mücadelesi, rakiplerini rahatsız etti ancak riskleri de beraberinde getirdi.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": -1 },
              "next_scene": "bolum_21"
            },
            "C": {
              "text": "Dengeleyici bir rol üstlen.",
              "outcome": "Dengeleyici yaklaşım, kısa vadede barışı sağladı fakat etkisi sınırlı kaldı.",
              "score_changes": { "harem": 0, "suleyman": 0, "divan": 1 },
              "next_scene": "bolum_21"
            }
          }
        },
        "bolum_21": {
          "description": "Hürrem, yeni ihanet iddiaları ve halkın şikayetleriyle yüzleşiyor. Adalet ve sadakat arasında kalıyor.",
          "options": {
            "A": {
              "text": "İhaneti kınayarak devlet bağlılığını göster.",
              "outcome": "İhaneti kınaması, devletin yanında olduğunu kanıtladı ancak düşmanlık yarattı.",
              "score_changes": { "harem": 1, "suleyman": 2, "divan": -1 },
              "next_scene": "bolum_22"
            },
            "B": {
              "text": "Halkın şikayetlerini dikkate al ve adaletli davran.",
              "outcome": "Halkın desteğini kazandı fakat bazı güçlü kişiler tarafından sorgulandı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_22"
            },
            "C": {
              "text": "Tarafsız kalarak durumu araştır.",
              "outcome": "Tarafsız yaklaşım, kısa vadede ortamı sakinleştirdi ama kesin sonuç vermedi.",
              "score_changes": { "harem": 0, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_22"
            }
          }
        },
        "bolum_22": {
          "description": "Sarayda Hürrem'e karşı söylentiler artıyor. Büyü iddiaları ve çevresindeki şüpheler doruğa ulaşıyor.",
          "options": {
            "A": {
              "text": "Söylentilere kayıtsız kal.",
              "outcome": "Kayıtsızlık kısa vadede sorun yaratmadı ancak uzun vadede güven kaybına yol açtı.",
              "score_changes": { "harem": 0, "suleyman": -1, "divan": 0 },
              "next_scene": "bolum_23"
            },
            "B": {
              "text": "Büyü iddialarına karşı açıklama yap.",
              "outcome": "Açıklaması bazı şüpheleri giderdi fakat rakipler tarafından sert eleştirildi.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": -1 },
              "next_scene": "bolum_23"
            },
            "C": {
              "text": "Söylentileri kendi avantajına çevir.",
              "outcome": "Büyü söylentilerini kullanarak rakiplerini korkutmayı başardı.",
              "score_changes": { "harem": 2, "suleyman": 0, "divan": 1 },
              "next_scene": "bolum_23"
            }
          }
        },
        "bolum_23": {
          "description": "Hürrem, Valide Sultan'ın emirleri ve aile baskılarıyla yüzleşiyor. İçsel çatışmalar derinleşiyor.",
          "options": {
            "A": {
              "text": "Valide Sultan'ın emirlerine itaat et.",
              "outcome": "İtaatkar davranarak saraydaki huzuru korudu, fakat özgürlüğünden ödün verdi.",
              "score_changes": { "harem": 1, "suleyman": -1, "divan": 0 },
              "next_scene": "bolum_24"
            },
            "B": {
              "text": "Emirleri manipüle ederek kendi çıkarlarını koru.",
              "outcome": "Manipülasyon, kısa vadede avantaj sağladı fakat riskleri de artırdı.",
              "score_changes": { "harem": 2, "suleyman": 0, "divan": 1 },
              "next_scene": "bolum_24"
            },
            "C": {
              "text": "Emirlere karşı açıkça meydan oku.",
              "outcome": "Açık meydan okuma, sarayda gerginlik yarattı ve düşmanlık arttı.",
              "score_changes": { "harem": -1, "suleyman": 1, "divan": -1 },
              "next_scene": "bolum_24"
            }
          }
        },
        "bolum_24": {
          "description": "Hürrem'in sanata ve kültüre olan ilgisi artıyor. Resim ve heykel gibi semboller üzerinden güç gösterisi gündemde.",
          "options": {
            "A": {
              "text": "Sultan'ın resmini beğen ve destekle.",
              "outcome": "Resmi destekleyerek Sultan'ın takdirini kazandı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 0 },
              "next_scene": "bolum_25"
            },
            "B": {
              "text": "Resmi eleştir ve geliştirme önerileri sun.",
              "outcome": "Eleştirileriyle zekasını ortaya koydu, ancak bazı çevrelerden tepki aldı.",
              "score_changes": { "harem": 0, "suleyman": 1, "divan": -1 },
              "next_scene": "bolum_25"
            },
            "C": {
              "text": "Resme kayıtsız kal ve riskleri azalt.",
              "outcome": "Kayıtsızlık, olası eleştirilerden kaçınmasını sağladı fakat fırsatları kaçırdı.",
              "score_changes": { "harem": -1, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_25"
            }
          }
        },
        "bolum_25": {
          "description": "Hürrem, saraydaki güç dengesini korumak için stratejik hamleler yapıyor. Kendi çocuklarının geleceği de tehlikede.",
          "options": {
            "A": {
              "text": "Çocuklarını destekle ve yetiştir.",
              "outcome": "Çocuklarına yatırım yaparak gelecekteki taht mücadelesine sağlam zemin hazırladı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_26"
            },
            "B": {
              "text": "Rakipleri yok etme planları yap.",
              "outcome": "Düşmanlarını bertaraf etmek için riskli hamleler yaptı.",
              "score_changes": { "harem": 2, "suleyman": 2, "divan": -2 },
              "next_scene": "bolum_26"
            },
            "C": {
              "text": "Bağımsız kalıp kendi planlarını uygula.",
              "outcome": "Kendi stratejisini uygulamaya koydu, fakat bu yalnızlık getirdi.",
              "score_changes": { "harem": -1, "suleyman": 0, "divan": -1 },
              "next_scene": "bolum_26"
            }
          }
        },
        "bolum_26": {
          "description": "Hürrem, sarayda yeni olaylarla yüzleşiyor. İhanet, dedikodular ve gizli operasyonlar arasında manevralar yapması gerekiyor.",
          "options": {
            "A": {
              "text": "İbrahim Paşa ile işbirliği yap.",
              "outcome": "Geçici ittifaklar kurarak bazı tehditleri bertaraf etti.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_27"
            },
            "B": {
              "text": "Gizli operasyonlarla rakipleri zayıflat.",
              "outcome": "Gizli hamlelerle rakiplerini şaşırttı fakat riskler arttı.",
              "score_changes": { "harem": 2, "suleyman": 0, "divan": -1 },
              "next_scene": "bolum_27"
            },
            "C": {
              "text": "Durumu olduğu gibi gözlemle ve risk alma.",
              "outcome": "Riskleri minimize ederek dengede kalmaya çalıştı.",
              "score_changes": { "harem": 0, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_27"
            }
          }
        },
        "bolum_27": {
          "description": "Devlet işlerinde yeni tehditler ortaya çıkıyor. Hürrem, saraydaki diplomatik ilişkileri yeniden değerlendiriyor.",
          "options": {
            "A": {
              "text": "Diplomatik ilişkileri güçlendir.",
              "outcome": "Yabancı elçilerle yakın ilişkiler kurarak avantaj sağladı.",
              "score_changes": { "harem": 1, "suleyman": 2, "divan": 1 },
              "next_scene": "bolum_28"
            },
            "B": {
              "text": "Rakipleriyle açık çatışmaya gir.",
              "outcome": "Açık çatışma, sarayda gerginlik yarattı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": -1 },
              "next_scene": "bolum_28"
            },
            "C": {
              "text": "Sessizce bekle ve uygun anı yakala.",
              "outcome": "Sabırlı yaklaşımı uzun vadede beklenmedik avantajlar getirdi.",
              "score_changes": { "harem": 1, "suleyman": 0, "divan": 1 },
              "next_scene": "bolum_28"
            }
          }
        },
        "bolum_28": {
          "description": "Hürrem, sarayda çocuklarının geleceği ve haremdeki güç dengesiyle ilgili kararlar almak zorunda.",
          "options": {
            "A": {
              "text": "Şehzade Mustafa'nın seferlere katılmasına izin ver.",
              "outcome": "Mustafa'nın askeri tecrübe kazanmasına fırsat tanıdı, ancak rekabeti artırdı.",
              "score_changes": { "harem": 0, "suleyman": 1, "divan": 0 },
              "next_scene": "bolum_29"
            },
            "B": {
              "text": "Mustafa'yı seferlerden uzak tut.",
              "outcome": "Mustafa'nın tecrübe kazanmasını engelledi, ancak aile içi gerilim yarattı.",
              "score_changes": { "harem": -1, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_29"
            },
            "C": {
              "text": "Orta yolu seç ve durumu dikkatle izle.",
              "outcome": "Dengeli yaklaşım, riskleri azaltırken fırsatları değerlendirmesine olanak sağladı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_29"
            }
          }
        },
        "bolum_29": {
          "description": "Sarayda yeni dedikodular ve ihanet iddiaları artıyor. Hürrem, bu durumun sonuçlarıyla yüzleşmeli.",
          "options": {
            "A": {
              "text": "İhanet iddialarını araştır.",
              "outcome": "Derinlemesine araştırma, gerçeği ortaya çıkardı ancak bazı rakipleri sinirlendirdi.",
              "score_changes": { "harem": 1, "suleyman": 0, "divan": 1 },
              "next_scene": "bolum_30"
            },
            "B": {
              "text": "İddiaları görmezden gel ve güç gösterisi yap.",
              "outcome": "Güç gösterisi, bazı çevreleri tatmin etti fakat riskleri artırdı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": -1 },
              "next_scene": "bolum_30"
            },
            "C": {
              "text": "Tarafsız kalarak ortamı gözlemle.",
              "outcome": "Gözlem, durumu anlamada yardımcı oldu fakat harekete geçmedi.",
              "score_changes": { "harem": 0, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_30"
            }
          }
        },
        "bolum_30": {
          "description": "Hürrem, artan siyasi belirsizlik ve ihanet korkusu arasında kritik bir karar vermeli.",
          "options": {
            "A": {
              "text": "Devlete bağlılığını güçlü şekilde göster.",
              "outcome": "Devlete olan bağlılığını açıkça ortaya koydu ve destek kazandı.",
              "score_changes": { "harem": 1, "suleyman": 2, "divan": 0 },
              "next_scene": "bolum_31"
            },
            "B": {
              "text": "Güç dengesini kendi lehine çevirmek için fırsatları değerlendir.",
              "outcome": "Fırsatları iyi değerlendirdi, ancak riskler de arttı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": -1 },
              "next_scene": "bolum_31"
            },
            "C": {
              "text": "Orta yolu seç ve dikkatlice hareket et.",
              "outcome": "Orta yaklaşım kısa vadede istikrar sağladı.",
              "score_changes": { "harem": 0, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_31"
            }
          }
        },
        "bolum_31": {
          "description": "Hürrem'in nikah meselesi ve saraydaki entrikalar yoğunlaşıyor. Kritik seçimler yapması gerekiyor.",
          "options": {
            "A": {
              "text": "Nikahı gerçekleştirmek için kararlı adımlar at.",
              "outcome": "Nikahı kıydırdı ve güçlenmeye başladı, ancak rakipleri öfkelenmeye başladı.",
              "score_changes": { "harem": 2, "suleyman": 2, "divan": -1 },
              "next_scene": "bolum_32"
            },
            "B": {
              "text": "Gizli yollarla nikahı tamamla.",
              "outcome": "Gizli işlemlerle nikahı halletti, ancak ifşa riski arttı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 0 },
              "next_scene": "bolum_32"
            },
            "C": {
              "text": "Nikah konusunda adım atmadan önce daha fazla bilgi topla.",
              "outcome": "Daha fazla bilgi topladı fakat fırsatlar kaçtı.",
              "score_changes": { "harem": 0, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_32"
            }
          }
        },
        "bolum_32": {
          "description": "Hürrem, kızının kaçırılması olayına tanık oluyor. İçsel çatışmalar ve intikam arzusu belirginleşiyor.",
          "options": {
            "A": {
              "text": "Kızını kurtarmak için acımasızca hareket et.",
              "outcome": "Acımasız hamlelerle kızını kurtarmaya çalıştı, ancak masumiyeti sorgulatabilecek adımlar attı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": -1 },
              "next_scene": "bolum_33"
            },
            "B": {
              "text": "Kızını kurtarmak için dikkatlice plan yap.",
              "outcome": "Planlı hareket ederek kızını kurtarma şansını artırdı, fakat zamanında adım atamadı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_33"
            },
            "C": {
              "text": "Durumu olduğu gibi kabul et ve intikam arzusunu bastır.",
              "outcome": "Kendi duygularını bastırdı, ancak bu yaklaşım uzun vadede risk oluşturdu.",
              "score_changes": { "harem": -1, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_33"
            }
          }
        },
        "bolum_33": {
          "description": "Hürrem, eğitim ve mektep açma meselesiyle ilgilenmeye başlar. Geleneksel ile modern arasında çatışma yaşanıyor.",
          "options": {
            "A": {
              "text": "Mektep açarak modern eğitim yöntemlerini destekle.",
              "outcome": "Modern eğitim anlayışını destekleyerek yenilikçi bir imaj çizdi.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_34"
            },
            "B": {
              "text": "Geleneksel değerlere sadık kal.",
              "outcome": "Geleneksel yaklaşıma bağlı kalarak eleştirileri minimize etti.",
              "score_changes": { "harem": 0, "suleyman": -1, "divan": 0 },
              "next_scene": "bolum_34"
            },
            "C": {
              "text": "Eğitim meselesini önemsemeyerek risk al.",
              "outcome": "Eğitime karşı kayıtsız kalması uzun vadede dezavantaj oluşturdu.",
              "score_changes": { "harem": -1, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_34"
            }
          }
        },
        "bolum_34": {
          "description": "Hürrem, sarayda gelişen hastalıklar, ölümler ve kişisel kayıplarla yüzleşiyor.",
          "options": {
            "A": {
              "text": "Hastalığa karşı yardım kampanyaları başlat.",
              "outcome": "Yardımseverliğiyle halkın takdirini kazandı, ancak zayıf yanlarını da gösterdi.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_35"
            },
            "B": {
              "text": "Kişisel kayıplar karşısında intikam peşine düş.",
              "outcome": "İntikam arzusu, çevresinde yeni düşmanlar oluşturdu.",
              "score_changes": { "harem": 2, "suleyman": 0, "divan": -2 },
              "next_scene": "bolum_35"
            },
            "C": {
              "text": "Kayıpları kabullen ve durumu analiz et.",
              "outcome": "Kabullenme, duygusal dayanıklılığını artırdı ancak harekete geçme isteğini azalttı.",
              "score_changes": { "harem": 0, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_35"
            }
          }
        },
        "bolum_35": {
          "description": "Sarayda çeşitli olaylar meydana geliyor: Kolyenin düşürülmesi, günlüğe ihtiyaç duyma, veba salgını ve Gül Ağa'nın kaçırılması.",
          "options": {
            "A": {
              "text": "Kolyeyi dikkatlice ara.",
              "outcome": "Kolyeyi bulduğunda önemli bir sırrın izlerini keşfetti.",
              "score_changes": { "harem": 1, "suleyman": 0, "divan": 1 },
              "next_scene": "bolum_36"
            },
            "B": {
              "text": "Günlüğü ele geçir.",
              "outcome": "Günlüğü elde ederek geçmişin gizemli sırlarını açığa çıkardı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": 0 },
              "next_scene": "bolum_36"
            },
            "C": {
              "text": "Veba salgınına karşı önlemler al ve Gül Ağa'nın durumunu sorgula.",
              "outcome": "Hastalığa karşı tedbir aldı ancak Gül Ağa olayını atladı.",
              "score_changes": { "harem": 0, "suleyman": -1, "divan": 0 },
              "next_scene": "bolum_36"
            }
          }
        },
        "bolum_36": {
          "description": "Hürrem, saray entrikaları ve kişisel ilişkilerle yeniden yüzleşiyor. İbrahim Paşa, Ressam Leo ve Validem'in gidişi gündemde.",
          "options": {
            "A": {
              "text": "İbrahim Paşa ile ilişkilerini güçlendir.",
              "outcome": "Paşa ile yakınlaşarak siyasi stratejilerini artırdı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_37"
            },
            "B": {
              "text": "Ressam Leo ile entelektüel bir bağ kur.",
              "outcome": "Sanat ve kültüre olan ilgisini kullanarak yeni perspektifler kazandı.",
              "score_changes": { "harem": 1, "suleyman": 0, "divan": 1 },
              "next_scene": "bolum_37"
            },
            "C": {
              "text": "Validem'in gidişine üzüntüyle tepki ver ve Gül Ağa'nın kaçırılmasını intikam için fırsat bil.",
              "outcome": "Duygusal tepkileri, saraydaki güç dengelerini değiştirebilecek riskler yarattı.",
              "score_changes": { "harem": 2, "suleyman": -1, "divan": -1 },
              "next_scene": "bolum_37"
            }
          }
        },
        "bolum_37": {
          "description": "Hürrem, prensese ve şehzade eğitimine dair politik hamleler yapmaya başlıyor. Rekabet ve strateji ön planda.",
          "options": {
            "A": {
              "text": "Prensese karşı rekabetçi ol.",
              "outcome": "Rekabetçi tutum, haremde gerginliği artırdı.",
              "score_changes": { "harem": 2, "suleyman": 0, "divan": -1 },
              "next_scene": "bolum_38"
            },
            "B": {
              "text": "Şehzade Mustafa'nın eğitimine önem ver.",
              "outcome": "Mustafa'nın eğitimine yatırım yaparak gelecekteki taht mücadelesinde avantaj sağladı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_38"
            },
            "C": {
              "text": "Politik olarak tarafsız kal ve gözlem yap.",
              "outcome": "Tarafsızlık kısa vadede güven sağladı, ancak etkisini azalttı.",
              "score_changes": { "harem": 0, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_38"
            }
          }
        },
        "bolum_38": {
          "description": "Hürrem, sarayda çeşitli tehditler ve kader tartışmalarıyla yüzleşiyor. Kaçırılma, suçlamalar ve tacın kaybı gündemde.",
          "options": {
            "A": {
              "text": "Kaçırılma olayına karşı direniş göster.",
              "outcome": "Direniş, riskli hamleler getirdi ancak hayatta kalma şansını artırdı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": -1 },
              "next_scene": "bolum_39"
            },
            "B": {
              "text": "Validem'in suçlamalarına karşı masumiyetini ispatla.",
              "outcome": "Masumiyetini ispatlayarak güven kazandı, ancak şüpheler devam etti.",
              "score_changes": { "harem": 1, "suleyman": 0, "divan": 1 },
              "next_scene": "bolum_39"
            },
            "C": {
              "text": "Tacın kaybını fırsata çevir ve yeni başlangıçlar yap.",
              "outcome": "Tacın kaybını avantaja çevirdi, fakat bu durum çevresinde şüpheler yarattı.",
              "score_changes": { "harem": 1, "suleyman": -1, "divan": 0 },
              "next_scene": "bolum_39"
            }
          }
        },
        "bolum_39": {
          "description": "Sarayda ölüm korkusu, artan rakip etkisi ve Macar tahtı meselesiyle yüzleşme zamanı. Kritik siyasi kararlar alınmalı.",
          "options": {
            "A": {
              "text": "Ölüm korkusuyla mücadele ederek güç kazan.",
              "outcome": "Ölüm korkusunu yenerek daha kararlı adımlar attı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": 0 },
              "next_scene": "bolum_40"
            },
            "B": {
              "text": "Pargalı'nın artan yetkilerine karşı sert önlemler al.",
              "outcome": "Pargalı ile çatışma riskleri arttı ancak kendi etkisini korudu.",
              "score_changes": { "harem": 1, "suleyman": -1, "divan": -1 },
              "next_scene": "bolum_40"
            },
            "C": {
              "text": "Macar tahtı meselesinde tarafını belirle.",
              "outcome": "Tarafını belirleyerek politik manevralara girişti, riskler de beraberinde geldi.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_40"
            }
          }
        },
        "bolum_40": {
          "description": "Hürrem, savaşın zorlukları, topların eksikliği, rakiplerin direnci ve aile meseleleriyle yüzleşiyor.",
          "options": {
            "A": {
              "text": "Savaşın getirdiği zorluklarla mücadele et ve metanetini koru.",
              "outcome": "Metanetli davranarak savaşın olumsuz etkilerini azaltmaya çalıştı.",
              "score_changes": { "harem": 1, "suleyman": 2, "divan": 0 },
              "next_scene": "bolum_41"
            },
            "B": {
              "text": "Topların eksikliğine yaratıcı çözümler bul.",
              "outcome": "Yaratıcı çözümlerle askeri eksiklikleri telafi etmeye çalıştı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_41"
            },
            "C": {
              "text": "Aile meselelerinde, özellikle Mustafa'nın seferlere katılmasına tepki göster.",
              "outcome": "Mustafa'nın seferlere katılması konusunda sert bir tutum sergiledi.",
              "score_changes": { "harem": 0, "suleyman": -1, "divan": -1 },
              "next_scene": "bolum_41"
            }
          }
        },
        "bolum_41": {
          "description": "Hürrem, saraydaki konumunu korumak için entrikalar, ittifaklar ve siyasi manevralar yapıyor. Doğu medeniyetine vakıf olma şartı da gündemde.",
          "options": {
            "A": {
              "text": "Saraydaki konumunu korumak için manipülasyon yap.",
              "outcome": "Manipülasyonla rakiplerini alt etti, ancak riskler de arttı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": -1 },
              "next_scene": "bolum_42"
            },
            "B": {
              "text": "Doğu medeniyetine vakıf olma şartını kendi çıkarları için kullan.",
              "outcome": "Bu şartı avantaja çevirerek etki alanını genişletti.",
              "score_changes": { "harem": 1, "suleyman": 0, "divan": 1 },
              "next_scene": "bolum_42"
            },
            "C": {
              "text": "Valide Sultan ile ilişkilerini yeniden şekillendir.",
              "outcome": "Valide Sultan ile ilişkilerini dengede tutmayı başardı.",
              "score_changes": { "harem": 1, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_42"
            }
          }
        },
        "bolum_42": {
          "description": "Hürrem, tehditler, nikah ilanı ve İbrahim Paşa'nın artan yetkileriyle yüzleşiyor. İntikam arzusu ve riskler ön planda.",
          "options": {
            "A": {
              "text": "Tehditleri bertaraf et ve intikam al.",
              "outcome": "Düşmanlarına karşı acımasız hamleler yaptı, intikam peşinde koştu.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": -2 },
              "next_scene": "bolum_43"
            },
            "B": {
              "text": "Nikah ilanı sonrası durumu yönet.",
              "outcome": "Nikahın getirdiği yeni sorumlulukları üstlenerek konumunu sağlamlaştırdı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 0 },
              "next_scene": "bolum_43"
            },
            "C": {
              "text": "İbrahim Paşa'nın etkisini azaltmak için strateji geliştir.",
              "outcome": "Stratejik hamlelerle İbrahim Paşa'yı kontrol altına almaya çalıştı.",
              "score_changes": { "harem": 1, "suleyman": 0, "divan": -1 },
              "next_scene": "bolum_43"
            }
          }
        },
        "bolum_43": {
          "description": "Hürrem, yeni statüsüne adaptasyon, İbrahim Paşa ile ilişkiler ve artan tehditlerle mücadele ediyor.",
          "options": {
            "A": {
              "text": "Yeni statüsüne güçlü bir şekilde adapte ol.",
              "outcome": "Yeni statüsünü benimseyerek saraydaki etkisini artırdı.",
              "score_changes": { "harem": 2, "suleyman": 2, "divan": 1 },
              "next_scene": "bolum_44"
            },
            "B": {
              "text": "İbrahim Paşa'ya karşı gizli entrikalar geliştir.",
              "outcome": "Gizli operasyonlarla İbrahim Paşa'nın etkisini azaltmayı başardı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": 0 },
              "next_scene": "bolum_44"
            },
            "C": {
              "text": "Tehditlere karşı savunma önlemleri al.",
              "outcome": "Güvenlik önlemleriyle hem kendini hem de ailesini korudu.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_44"
            }
          }
        },
        "bolum_44": {
          "description": "Hürrem, saraydaki güç dengelerini korumak için çeşitli taktikler uygular. Taç tartışması ve harem içi düzenlemeler gündemde.",
          "options": {
            "A": {
              "text": "Güç dengelerini korumak için rakiplerine karşı agresif davran.",
              "outcome": "Agresif tavrı, bazı rakiplerini etkisiz hale getirdi ancak düşman çevresini genişletti.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": -1 },
              "next_scene": "bolum_45"
            },
            "B": {
              "text": "Aile içi ilişkileri güçlendir ve haremde dengeyi sağla.",
              "outcome": "Aile içi ittifaklar, saraydaki kontrolünü artırdı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_45"
            },
            "C": {
              "text": "Devlet işlerinde aktif rol al.",
              "outcome": "Devlet adamlarıyla yakın ilişkiler kurarak siyasi gücünü pekiştirdi.",
              "score_changes": { "harem": 1, "suleyman": 2, "divan": 0 },
              "next_scene": "bolum_45"
            }
          }
        },
        "bolum_45": {
          "description": "Süleyman'ın sefere çıkmasıyla sarayda oluşan boşluk, Hürrem'in stratejilerini şekillendiriyor. Çocuklarının geleceği, aile ve harem rekabeti önem kazanıyor.",
          "options": {
            "A": {
              "text": "Süleyman'ın yokluğunda gücü koru ve artır.",
              "outcome": "Yeni ittifaklar kurdu ve rakiplerini zayıflattı.",
              "score_changes": { "harem": 2, "suleyman": 2, "divan": 0 },
              "next_scene": "bolum_46"
            },
            "B": {
              "text": "Çocuklarının geleceğini güvence altına al.",
              "outcome": "Çocuklarının eğitimine ve evliliklerine odaklanarak gelecek için sağlam adımlar attı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_46"
            },
            "C": {
              "text": "Valide Sultan ile ilişkileri yeniden şekillendir.",
              "outcome": "Valide Sultan ile uyumlu hareket ederek saraydaki gerilimi azalttı.",
              "score_changes": { "harem": 1, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_46"
            }
          }
        },
        "bolum_46": {
          "description": "Süleyman'ın seferleri devam ederken, Hürrem sarayda artan entrikalarla ve duygusal çatışmalarla yüzleşiyor.",
          "options": {
            "A": {
              "text": "Süleyman'ın yokluğunda gücü kontrol altında tut.",
              "outcome": "Güç boşluğunu doldurmak için stratejik hamleler yaptı.",
              "score_changes": { "harem": 2, "suleyman": 2, "divan": 0 },
              "next_scene": "bolum_47"
            },
            "B": {
              "text": "Çocuklarına odaklan ve onları güçlendir.",
              "outcome": "Çocuklarına yatırım yaparak gelecekteki taht mücadelesinde avantaj sağladı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_47"
            },
            "C": {
              "text": "Haremdeki rekabeti acımasızca yönlendir.",
              "outcome": "Rakiplerine karşı sert önlemler aldı, fakat bu durum çevresinde yeni düşmanlar yarattı.",
              "score_changes": { "harem": 2, "suleyman": 0, "divan": -1 },
              "next_scene": "bolum_47"
            }
          }
        },
        "bolum_47": {
          "description": "Hürrem, devlet işlerinde ve harem rekabetinde daha aktif bir rol almaya başlıyor. Politik manevralar ve intikam arzusu ön planda.",
          "options": {
            "A": {
              "text": "Çocuklarının geleceğini güvence altına al.",
              "outcome": "Stratejik adımlarla çocuklarını destekleyip geleceğe hazırladı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_48"
            },
            "B": {
              "text": "Valide Sultan'a karşı strateji belirle.",
              "outcome": "Valide Sultan ile olan ilişkilerinde kendi çıkarlarını korumak için dikkatli hamleler yaptı.",
              "score_changes": { "harem": 1, "suleyman": 0, "divan": 0 },
              "next_scene": "bolum_48"
            },
            "C": {
              "text": "Haremdeki gücü sağlamlaştır.",
              "outcome": "Haremdeki rakiplerini geride bırakarak kendi etkisini artırdı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": 0 },
              "next_scene": "bolum_48"
            }
          }
        },
        "bolum_48": {
          "description": "Hürrem, devletin ve saraydaki güç dengelerinin geleceğini belirlemek için kritik kararlar alıyor.",
          "options": {
            "A": {
              "text": "Çocuklarının geleceği için aktif mücadeleye devam et.",
              "outcome": "Çocuklarının eğitimine ve stratejik evliliklere odaklandı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_49"
            },
            "B": {
              "text": "Devlet işlerine daha fazla müdahil ol.",
              "outcome": "Süleyman'ın kararlarına etki ederek devlet yönetiminde etkin rol aldı.",
              "score_changes": { "harem": 1, "suleyman": 2, "divan": 0 },
              "next_scene": "bolum_49"
            },
            "C": {
              "text": "Haremdeki rekabeti acımasızca sürdür.",
              "outcome": "Rakiplerini etkisiz hale getirerek kendi gücünü pekiştirdi.",
              "score_changes": { "harem": 2, "suleyman": 0, "divan": -1 },
              "next_scene": "bolum_49"
            }
          }
        },
        "bolum_49": {
          "description": "Sarayda son kararlar alınıyor. Hürrem, tüm stratejilerini gözden geçirip son hamlelerini yapmalı.",
          "options": {
            "A": {
              "text": "Şehzade Mustafa'yı kontrol altına al ve rakiplerden uzak tut.",
              "outcome": "Mustafa'yı izleyerek siyasi gücünü sınırlandırdı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": 0 },
              "next_scene": "bolum_50"
            },
            "B": {
              "text": "Valide Sultan ile ilişkileri güçlendir.",
              "outcome": "Valide Sultan ile bağlarını güçlendirerek saraydaki güvenini tazeledi.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_50"
            },
            "C": {
              "text": "İbrahim Paşa'ya karşı hamle yap ve onu etkisiz hale getir.",
              "outcome": "Stratejik hamlelerle İbrahim Paşa'nın etkisini azaltmayı başardı.",
              "score_changes": { "harem": 2, "suleyman": 0, "divan": -1 },
              "next_scene": "bolum_50"
            }
          }
        }, "bolum_50": {
          "description": "Saraydaki nihai karar zamanı. Hürrem, çocuklarının geleceği, haremdeki güç dengesi ve devlet işlerine dair son stratejilerini belirliyor.",
          "options": {
            "A": {
              "text": "Mustafa'nın evliliğini sabote et.",
              "outcome": "Mustafa'nın evliliğini engellemeye çalışarak, kendi çocuklarının geleceğini güvence altına aldı.",
              "score_changes": { "harem": 2, "suleyman": 1, "divan": 0 },
              "next_scene": "bolum_51"
            },
            "B": {
              "text": "Kendi çocuklarının eğitimine ve evliliklerine odaklan.",
              "outcome": "Kendi çocuklarına yatırım yaparak güçlü bir gelecek inşa etmeye çalıştı.",
              "score_changes": { "harem": 1, "suleyman": 1, "divan": 1 },
              "next_scene": "bolum_51"
            },
            "C": {
              "text": "Süleyman üzerindeki etkisini sürdür ve devlet işlerinde aktif rol al.",
              "outcome": "Süleyman'ı yönlendirerek devlet işlerine etki etmeye devam etti.",
              "score_changes": { "harem": 2, "suleyman": 2, "divan": 0 },
              "next_scene": "bolum_51"
            }
          }
        },
            "bolum_51": {
                "description": "Bolum 51: Hürrem, İbrahim Paşa'nın canı mevzu bahis olduğunda Valide Sultan (Hatice Sultan) karşısında bir kırılma yaşıyor. Aynı zamanda Gülfem Hatun'un huzursuzluğu, Mahidevran ve Fatma Hatun ile ilgili entrikalar da gündemde.",
                "character": {
                    "name": "Hatice Sultan",
                    "image": "images/hatice_sultan.png",
                    "quote": "İftira attıysa, ben bunu kabul edemem!"
                },
                "options": {
                    "A": {
                        "text": "Valide Sultan'ı dinle, geri çekil.",
                        "outcome": "Süleyman'ın gözünde daha az hırslı görünürsünüz, fakat İbrahim'in hayatı tehlikeye girer.",
                        "score_changes": {"harem": -1, "suleyman": -1, "divan": 0},
                        "next_scene": "bolum_52"
                    },
                    "B": {
                        "text": "Valide Sultan'a karşı gel, entrikaları sürdür.",
                        "outcome": "Süleyman'ın gözünde cesur ve sadık görünürsünüz, ancak Valide Sultan'ın düşmanlığını kazanırsınız.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": -1},
                        "next_scene": "bolum_52"
                    },
                    "C": {
                        "text": "Valide Sultan ile uzlaşmaya çalış.",
                        "outcome": "Dengeli bir yaklaşım benimsersiniz; hem İbrahim’i kurtarmaya çalışır hem de Valide Sultan’ın öfkesini yatıştırmaya çalışırsınız, fakat başarı şansı düşük kalır.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_52"
                    }
                }
            },
            "bolum_52": {
                "description": "Bolum 52: Hürrem, Süleyman ile karşılaşır; sancağa gideceğini öğrenir. Aynı zamanda İbrahim Paşa'nın Doğu seferi hazırlığı ve Matrakçı'nın sefer zamanı gündemde.",
                "character": {
                    "name": "Süleyman",
                    "image": "images/suleyman.jpg",
                    "quote": "Benim yolum buradan geçecek!"
                },
                "options": {
                    "A": {
                        "text": "Süleyman'a sitem et, gitmesini engelle.",
                        "outcome": "Baskıcı ve kontrolcü bir tutum sergilersiniz.",
                        "score_changes": {"harem": -1, "suleyman": -1, "divan": 0},
                        "next_scene": "bolum_53"
                    },
                    "B": {
                        "text": "Süleyman'ın kararına saygı gösterir gibi görün, ama ima edersiniz.",
                        "outcome": "Süleyman, içten duygularınızı anlar ve etkilenir.",
                        "score_changes": {"harem": 0, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_53"
                    },
                    "C": {
                        "text": "Süleyman'ın kararına tamamen kayıtsız kal.",
                        "outcome": "Süleyman'ın Hürrem'e olan ilgisi azalır.",
                        "score_changes": {"harem": -1, "suleyman": -2, "divan": 0},
                        "next_scene": "bolum_53"
                    }
                }
            },
            "bolum_53": {
                "description": "Bolum 53: Hürrem, cariyesi Esma'nın davranışlarından şüphelenir; Şehzade Mustafa'nın zehirlenmiş olabileceği şüphesiyle yüzleşir; ayrıca Süleyman'ın Gülbahar Hatun'la konuşmasına şahit olur ve sevgisinden şüphe duymaya başlar.",
                "character": {
                    "name": "Şahzade Mustafa",
                    "image": "images/mustafa.png",
                    "quote": "Benim sağlığım her şeyden önemli!"
                },
                "options": {
                    "A": {
                        "text": "Esma'ya sert davranıp sorgula.",
                        "outcome": "Esma korkar, belki yalan söylemeye başlar.",
                        "score_changes": {"harem": 1, "suleyman": -1, "divan": 0},
                        "next_scene": "bolum_57"
                    },
                    "B": {
                        "text": "Esma'ya şefkatle yaklaş, güven ver.",
                        "outcome": "Esma açılarak gerçekleri paylaşır.",
                        "score_changes": {"harem": 2, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_57"
                    },
                    "C": {
                        "text": "Esma'yı gözlemlemeye devam et.",
                        "outcome": "Temkinli hareket ettiniz ancak bilgi toplamak uzun sürdü.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_57"
                    }
                }
            },
            "bolum_57": {
                "description": "Bolum 57: Hürrem, Gülfem'in huzursuz olduğunu öğrenir; ayrıca Daye Hatun yerine yeni hazinedar seçme kararsızlığı ve Matrakçı'nın Doğu seferiyle ilgili durumu gündeme gelir.",
                "character": {
                    "name": "Gülfem Hatun",
                    "image": "images/gulfem.png",
                    "quote": "Bu huzursuzluk basit bir belirtiden öte..."
                },
                "options": {
                    "A": {
                        "text": "Gülfem'i doğrudan sorgula.",
                        "outcome": "Gülfem, sorgu altında korkabilir ve yalan söylemeye başlayabilir.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": -1},
                        "next_scene": "bolum_59"
                    },
                    "B": {
                        "text": "Gülfem'e anlayışlı yaklaş, destek ol.",
                        "outcome": "Gülfem içtenlikle gerçeği paylaştı.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_59"
                    },
                    "C": {
                        "text": "Gülfem'i gözlemlemeye devam et.",
                        "outcome": "Uzun süre gözlemlediniz, bilgi toplamak zaman aldı.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_59"
                    }
                }
            },
            "bolum_59": {
                "description": "Bolum 59: Hürrem, Paşa'nın kendisini eş değerde gördüğü, Fatma Hatun'un entrikaları ve kendisine yönelik iftiralara karşı nasıl tepki vereceğini değerlendiriyor.",
                "character": {
                    "name": "Ebu Suud",
                    "image": "images/ebusuud.png",
                    "quote": "Güç, sözde değil eylemdedir!"
                },
                "options": {
                    "A": {
                        "text": "Paşa'yı uyar, sınırlarını aşmaması gerektiğini bildir.",
                        "outcome": "Paşa'ya sınır koyduğunuz anlaşıldı.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_66"
                    },
                    "B": {
                        "text": "Fatma Hatun'u açıkça tehdit et.",
                        "outcome": "Fatma Hatun, tehditler karşısında geri çekildi.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": -1},
                        "next_scene": "bolum_66"
                    },
                    "C": {
                        "text": "İftiralara karşı sessiz kal, bekle.",
                        "outcome": "Sessiz kalmak durumu izlemek için seçildi.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_66"
                    }
                }
            },
            "bolum_66": {
                "description": "Bolum 66: Hürrem, Paşa'nın Bağdat'a gitmekte kararlı olduğunu, İskender'in düzmece istihbaratını ve askere sirayet edecek husumeti öğreniyor.",
                "character": {
                    "name": "Pargalı",
                    "image": "images/pargali.png",
                    "quote": "Bağdat yolunda tehlike var, dikkat etmeliyiz!"
                },
                "options": {
                    "A": {
                        "text": "Paşa'yı ikna etmeye çalış.",
                        "outcome": "Paşa'nın kararını değiştirmeye çalıştınız.",
                        "score_changes": {"harem": 0, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_67"
                    },
                    "B": {
                        "text": "Paşa'nın gitmesine izin ver, fakat yakından takip et.",
                        "outcome": "Güvenilir bir temsilci atayarak durumu kontrol altına aldınız.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_67"
                    },
                    "C": {
                        "text": "Durumu kabullen, Paşa'nın kararına saygı göster.",
                        "outcome": "Sakin bir tutum sergilediniz.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_67"
                    }
                }
            },
            "bolum_67": {
                "description": "Bolum 67: Hürrem, haremi koruma vazifesini, Nadya'nın tepkisini ve ayrılık-ecel konularını değerlendiriyor.",
                "character": {
                    "name": "Mihrimah",
                    "image": "images/mihrimah.png",
                    "quote": "Kalbim, kaderin acımasız oyunlarına yenik düşmemeli!"
                },
                "options": {
                    "A": {
                        "text": "Haremi ciddiye alıp koruma görevini yerine getir.",
                        "outcome": "Sorumluluk bilinciyle haremi kontrol altında tuttunuz.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_68"
                    },
                    "B": {
                        "text": "Nadya'yı sorgula ve neden hayrete düştüğünü öğren.",
                        "outcome": "Nadya'nın davranışlarını analiz ettiniz.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_68"
                    },
                    "C": {
                        "text": "Ayrılık ve ecel üzerine derin düşüncelere dal.",
                        "outcome": "İnancınızı koruyarak derin düşüncelere daldınız.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_68"
                    }
                }
            },
            "bolum_68": {
                "description": "Bolum 68: Hürrem, cariyenin zor durumda olduğunu öğrenir ve yaklaşan akıbeti bir fırsata çevirmeyi düşünür.",
                "character": {
                    "name": "Bali Bey",
                    "image": "images/bali_bey.png",
                    "quote": "Güç, her zaman kendi lehimize işler."
                },
                "options": {
                    "A": {
                        "text": "Cariyeye yardım et.",
                        "outcome": "Merhametli davranıp destek verdiniz.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_69"
                    },
                    "B": {
                        "text": "Durumu umursamaz, kendi planlarına odaklan.",
                        "outcome": "Kendi çıkarlarınızı ön planda tuttunuz, fakat bu durum eleştiriye yol açabilir.",
                        "score_changes": {"harem": -1, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_69"
                    },
                    "C": {
                        "text": "Akıbeti fırsata çevirip plan yap.",
                        "outcome": "Stratejik planlar geliştirdiniz ve fırsat yarattınız.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_69"
                    }
                }
            },
            "bolum_69": {
                "description": "Bolum 69: Hürrem, Mehmet'in ata binmekten korktuğunu öğrenir ve validemin yüzünün nihayet güldüğünü fark eder.",
                "character": {
                    "name": "Bali Bey",  
                    "image": "images/bali_bey.png",
                    "quote": "Korku, cesaretin düşmanıdır."
                },
                "options": {
                    "A": {
                        "text": "Mehmet'i cesaretlendir, ata binmesine yardım et.",
                        "outcome": "Mehmet'in korkusunu yenmesine destek oldunuz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_70"
                    },
                    "B": {
                        "text": "Mehmet'in korkusunu küçümseyip zorla ata bindirmeye çalış.",
                        "outcome": "Otoriter bir tutum sergilediniz, fakat riskli sonuçlar doğurdu.",
                        "score_changes": {"harem": -1, "suleyman": -1, "divan": 0},
                        "next_scene": "bolum_70"
                    },
                    "C": {
                        "text": "Mehmet'in korkusunu anla ve alternatif aktiviteler sun.",
                        "outcome": "Anlayışlı davrandınız, ortamda yumuşaklık sağladınız.",
                        "score_changes": {"harem": 0, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_70"
                    }
                }
            },
            "bolum_70": {
                "description": "Bolum 70: Hürrem, evleneceği adamı başka bir yere gönderme teklifiyle ve Cihangir'in rahatsızlığıyla karşı karşıya.",
                "character": {
                    "name": "Cihangir",
                    "image": "images/cihangir.png",
                    "quote": "Rahatsızlık bazen gizli tehlikelerin habercisidir."
                },
                "options": {
                    "A": {
                        "text": "Evleneceği adamı gönder, uygulamayı yap.",
                        "outcome": "Gücünüzü ve kontrolünüzü net bir şekilde gösterdiniz.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_71"
                    },
                    "B": {
                        "text": "Sadece blöf yap, ama adamı göndermeyin.",
                        "outcome": "Stratejik zekanızı ortaya koyarak blöf yaptınız.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_71"
                    },
                    "C": {
                        "text": "Kararınızdan vazgeçin.",
                        "outcome": "Durumu kabullenip ısrarcı davranmadınız.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_71"
                    }
                }
            },
            "bolum_71": {
                "description": "Bolum 71: Hürrem, Şehzade Bayezid'in Kütahya'ya gitmek istememesi ve Atmaca'nın gelişi üzerine stratejik kararlar almalı.",
                "character": {
                    "name": "Şehzade Bayezid",
                    "image": "images/bayezid.png",
                    "quote": "Kütahya'ya gitmek, kalbimin sesini dinlemek demektir."
                },
                "options": {
                    "A": {
                        "text": "Önceliklerinizi belirleyip Bayezid'in kararını etkilemeye çalışın.",
                        "outcome": "Stratejik adımlarla Bayezid'in kararını etkilediniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_108"
                    },
                    "B": {
                        "text": "Her iki durumu da dengeleyin.",
                        "outcome": "Karma strateji benimsediniz, dengede kalmaya çalıştınız.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_108"
                    },
                    "C": {
                        "text": "Sadece Bayezid'in kararlarına odaklanın.",
                        "outcome": "Tek taraflı strateji risk oluşturdu.",
                        "score_changes": {"harem": -1, "suleyman": -1, "divan": 0},
                        "next_scene": "bolum_108"
                    }
                }
            },
            "bolum_108": {
                "description": "Bolum 108: Evlilik ve Kapudan Paşa'nın kızı konusu gündemde. Evlilikler politik araç olarak değerlendiriliyor.",
                "character": {
                    "name": "Kapudan Paşa'nın Kızı",
                    "image": "images/kapudan_kizi.png",
                    "quote": "Ben, sarayın yeni penceresiyim."
                },
                "options": {
                    "A": {
                        "text": "İttifakları değerlendirin.",
                        "outcome": "Stratejik ittifaklar kurarak avantaj sağladınız.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_109"
                    },
                    "B": {
                        "text": "Evlilikleri politik araç olarak kullanın.",
                        "outcome": "Çıkar ilişkilerinizi güçlendirerek avantaj sağladınız.",
                        "score_changes": {"harem": 2, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_109"
                    },
                    "C": {
                        "text": "Her iki stratejiyi de uygulayın.",
                        "outcome": "Karma strateji benimsediniz; riskler ve avantajlar beraberinde geldi.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_109"
                    }
                }
            },
            "bolum_109": {
                "description": "Bolum 109: Hakikat, ateş ve derya kavramları üzerine derin düşünceler; Mustafa Paşa’dan intikam arzusu ve aile bağları tartışılıyor.",
                "character": {
                    "name": "Mustafa Paşa",
                    "image": "images/mustafa_pasa.png",
                    "quote": "Adaletin tereddüdü, intikamın kıvılcımıdır."
                },
                "options": {
                    "A": {
                        "text": "Hakikati arayın.",
                        "outcome": "Derin düşüncelerle gerçekleri sorguladınız.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_110"
                    },
                    "B": {
                        "text": "İntikam duygunuzu analiz edin.",
                        "outcome": "İntikam arzunuzu değerlendirdiniz, bazı riskler hissettiniz.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_110"
                    },
                    "C": {
                        "text": "Dış ilişkileri yakından takip edin.",
                        "outcome": "Diplomatik ilişkileri güçlendirmeye çalıştınız.",
                        "score_changes": {"harem": 0, "suleyman": 2, "divan": 0},
                        "next_scene": "bolum_110"
                    }
                }
            },
            "bolum_110": {
                "description": "Bolum 110: Venedik balosu, dostluk ve cephe genişlemesi konusu; 'Hünkar böyle karar vermiş...' sözüyle Hürrem'in manipülatif yönü öne çıkıyor.",
                "character": {
                    "name": "Hünkar",
                    "image": "images/hunkar.png",
                    "quote": "Güç, her daim adil olmalı."
                },
                "options": {
                    "A": {
                        "text": "İtibarınızı koruyun.",
                        "outcome": "Hünkar'ın kararını destekleyerek itibarınızı güçlendirdiniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "final"
                    },
                    "B": {
                        "text": "Oyun içinde oyun oynayın, planlarınızı devreye sokun.",
                        "outcome": "Kendi planlarınızı uygulayarak stratejik avantaj sağladınız.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": 1},
                        "next_scene": "final"
                    },
                    "C": {
                        "text": "Etki alanınızı genişletin.",
                        "outcome": "Seferde yer alacak kişilerle ilişkilerinizi geliştirip etki alanınızı artırdınız.",
                        "score_changes": {"harem": 2, "suleyman": 2, "divan": 0},
                        "next_scene": "final"
                    }
                }
            },
            "final": {
                "description": "Oyun sona erdi. Hürrem Sultan'ın saraydaki yolculuğu tamamlandı. Geçmiş seçimlerinizin sonuçları ortaya çıktı.",
                "options": {}
            }
            # ------------------------------------------------------------------------------------
            # Bolum 92'den 105'e ve devamı: Aşağıda özet örnekler verilmiştir. (Her bölüm için yukarıdaki örnek formatı tekrarlanacak.)
            ,
            "bolum_92": {
                "description": "Bolum 92: Mira'nın ihaneti ve evlendirme telaşı; Paşa hazretlerinin sözleri gündemde.",
                "character": {
                    "name": "Mira",
                    "image": "images/mira.png",
                    "quote": "Benim ihanetime kimse mazhar olmaz!"
                },
                "options": {
                    "A": {
                        "text": "Mira'nın ihanetine öfkeyle karşılık ver, cezalandır.",
                        "outcome": "Öfkeyle sert cezalar uyguladınız.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": -1},
                        "next_scene": "bolum_93"
                    },
                    "B": {
                        "text": "Durumu analiz edip stratejik yaklaşım sergile.",
                        "outcome": "İhanetin altındaki nedenleri çözümlüyorsunuz.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_93"
                    },
                    "C": {
                        "text": "Olayı görmezden gel, evlendirme telaşına katıl.",
                        "outcome": "Pragmatik bir tutum benimsediniz, riskler devam etti.",
                        "score_changes": {"harem": 0, "suleyman": -1, "divan": 0},
                        "next_scene": "bolum_93"
                    },
                    "D": {
                        "text": "Paşa hazretlerinin sözlerine hemen müdahale et.",
                        "outcome": "Acil önlemlerle duruma müdahale ettiniz.",
                        "score_changes": {"harem": 1, "suleyman": 2, "divan": -1},
                        "next_scene": "bolum_93"
                    },
                    "E": {
                        "text": "Durumu gözlemleyip sonra müdahale et.",
                        "outcome": "Sabırlı stratejinizle harekete geçtiniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_93"
                    }
                }
            },
            "bolum_93": {
                "description": "Bolum 93: Şehzade'nin kaybolması, kıyafetlerinin bulunması; Validemin 'yemin ederim kazaydı' demesi gündemde.",
                "character": {
                    "name": "Hünkar",
                    "image": "images/hunkar.png",
                    "quote": "Her şey kaderin bir oyunu..."
                },
                "options": {
                    "A": {
                        "text": "Panik halinde arama çalışmalarına katıl.",
                        "outcome": "Kendi çabalarınızla arama çalışmalarına dahil oldunuz.",
                        "score_changes": {"harem": 2, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_94"
                    },
                    "B": {
                        "text": "Arama çalışmalarını uzaktan yönetin.",
                        "outcome": "Uzaktan kontrol sağlayarak riskleri azalttınız.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_94"
                    },
                    "C": {
                        "text": "Olayı politik fırsata dönüştürmeye çalışın.",
                        "outcome": "Durumu kendi çıkarınız için kullanmaya başladınız.",
                        "score_changes": {"harem": 2, "suleyman": -1, "divan": 1},
                        "next_scene": "bolum_94"
                    },
                    "D": {
                        "text": "Validemin açıklamasını kabul edip olayı kapatın.",
                        "outcome": "Olayı kabul ederek tartışmalardan kaçındınız.",
                        "score_changes": {"harem": 0, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_94"
                    },
                    "E": {
                        "text": "Şüphelenip gizlice soruşturma başlatın.",
                        "outcome": "Gizli soruşturma başlattınız, riskli bir hamle oldu.",
                        "score_changes": {"harem": 1, "suleyman": -1, "divan": 1},
                        "next_scene": "bolum_94"
                    },
                    "F": {
                        "text": "Olayı cezalandırıp ders vermeye çalışın.",
                        "outcome": "Açık cezalandırma ile mesaj verdiniz.",
                        "score_changes": {"harem": -1, "suleyman": 0, "divan": -1},
                        "next_scene": "bolum_94"
                    }
                }
            },
            "bolum_94": {
                "description": "Bolum 94: Donanmanın yokluğu ve portakal korsanlarından bahsediliyor.",
                "options": {
                    "A": {
                        "text": "Korsanlarla mücadele et.",
                        "outcome": "Askeri güç kullanarak korsanlara karşı harekete geçtiniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_95"
                    },
                    "B": {
                        "text": "Borçları kapatmak için evrak verin.",
                        "outcome": "Borçlarınızı ödeyip itibarınızı korumaya çalıştınız.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_95"
                    },
                    "C": {
                        "text": "Fırsatları değerlendirin, strateji geliştirin.",
                        "outcome": "Ekonomik ve siyasi avantajlar elde ettiniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_95"
                    }
                }
            },
            "bolum_95": {
                "description": "Bolum 95: Hürrem, borcunu kapatır, evrak alır; bu durum şehzadenin geleceği ve veba salgını ile ilişkilidir.",
                "options": {
                    "A": {
                        "text": "Borçlarınızı ödeyip evrakı kabul edin.",
                        "outcome": "İtibarınızı korudunuz, fakat zayıflık gösterdiniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_96"
                    },
                    "B": {
                        "text": "Farklı stratejiler geliştirip borcu kapatmaya çalışın.",
                        "outcome": "Riskli hamlelerle borçlarınızı ödemeye çalıştınız.",
                        "score_changes": {"harem": 2, "suleyman": 0, "divan": -1},
                        "next_scene": "bolum_96"
                    },
                    "C": {
                        "text": "Evrakı kendi çıkarınız için kullanın.",
                        "outcome": "Manipülatif hamlelerle evrakı avantaja çevirdiniz.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_96"
                    }
                }
            },
            "bolum_96": {
                "description": "Bolum 96: Veba salgınına karşı tedbirler alınması, Lütfü Paşa'nın askeri teftişi ve Şeyh Maşuki meselesi gündemde.",
                "options": {
                    "A": {
                        "text": "Veba salgınına karşı önlemler alın.",
                        "outcome": "Salgını kontrol altına almaya çalıştınız.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_97"
                    },
                    "B": {
                        "text": "Lütfü Paşa'nın faaliyetlerini yakından izleyin.",
                        "outcome": "Askeri stratejileri değerlendirdiniz.",
                        "score_changes": {"harem": 0, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_97"
                    },
                    "C": {
                        "text": "Şeyh Maşuki meselesini kendi çıkarlarınız için kullanın.",
                        "outcome": "Siyasi avantajlar elde etmek için harekete geçtiniz.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_97"
                    }
                }
            },
            "bolum_97": {
                "description": "Bolum 97: Şah Sultan'ın hafife alınması ve Hürrem'in önemi vurgulanıyor. Gelecek stratejileri için ipuçları mevcut.",
                "options": {
                    "A": {
                        "text": "Şah Sultan'ın gücünü hesaba katarak hareket edin.",
                        "outcome": "Dikkatli ve stratejik adımlar attınız.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_98"
                    },
                    "B": {
                        "text": "Osman'ın sağlık durumunu yakından takip edin.",
                        "outcome": "Sağlık konusuna odaklandınız.",
                        "score_changes": {"harem": 0, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_98"
                    },
                    "C": {
                        "text": "Her iki konuyu da dikkate alarak strateji geliştirin.",
                        "outcome": "Karma strateji benimsediniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_98"
                    }
                }
            },
            "bolum_98": {
                "description": "Bolum 98: Lütfi Paşa ile ilgili dedikodular ve politik entrikalar gündemde.",
                "options": {
                    "A": {
                        "text": "Dedikodunun aslına bakın.",
                        "outcome": "Gerçekleri ortaya çıkarmaya çalıştınız.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_99"
                    },
                    "B": {
                        "text": "Lütfi Paşa'yı kontrol altına alın.",
                        "outcome": "Siyasi kontrolü ele geçirmeye çalıştınız.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_99"
                    },
                    "C": {
                        "text": "Durumu kendi çıkarınız için kullanın.",
                        "outcome": "Manipülatif hamlelerle avantaj sağladınız.",
                        "score_changes": {"harem": 2, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_99"
                    }
                }
            },
            "bolum_99": {
                "description": "Bolum 99: Düğün şenlikleri ve Paşa'nın saraya gidişi gündemde. Paşa'nın hareketlerini kontrol etmeye çalışıyorsunuz. Aynı zamanda Hünkar'ın vazifesi icabı bir hadiseyi bildirmesi potansiyel tehdit oluşturuyor.",
                "options": {
                    "A": {
                        "text": "Paşa'nın her adımını yakından izleyin.",
                        "outcome": "Bilgi akışını sıkı kontrol altına aldınız.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_100"
                    },
                    "B": {
                        "text": "Paşa'yı kendi çıkarınız için kullanın.",
                        "outcome": "Stratejik avantajlar elde ettiniz.",
                        "score_changes": {"harem": 2, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_100"
                    },
                    "C": {
                        "text": "Paşa'yı gözlemleyin, bilgi toplayın.",
                        "outcome": "Daha temkinli bir yaklaşım benimsediniz.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_100"
                    },
                    "D": {
                        "text": "Hadisenin ne olduğunu öğrenmek için harekete geçin.",
                        "outcome": "Potansiyel tehlikeyi bertaraf etmek adına adım attınız.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_100"
                    }
                }
            },
            "bolum_100": {
                "description": "Bolum 100: Bali Bey'in uğursuzluk getireceği inancı ve yeni yayın/ok tanıtımları gündemdedir.",
                "options": {
                    "A": {
                        "text": "Batıl inançlara karşı temkinli davranın.",
                        "outcome": "Dini inançlara dikkat ederek temkinli adımlar attınız.",
                        "score_changes": {"harem": 0, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_101"
                    },
                    "B": {
                        "text": "Askeri gücü artırma potansiyelini değerlendirin.",
                        "outcome": "Askeri stratejilere odaklanarak avantaj sağladınız.",
                        "score_changes": {"harem": 1, "suleyman": 2, "divan": 0},
                        "next_scene": "bolum_101"
                    },
                    "C": {
                        "text": "Her iki stratejiyi de uygulayın.",
                        "outcome": "Karma strateji benimsediniz; riskler arttı ancak avantajlar elde ettiniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_101"
                    }
                }
            },
            "bolum_101": {
                "description": "Bolum 101: Evran Şah Sultan'ın boşanmak istemesi ve Lütfü Paşa'nın Divanda olmaması, Hürrem için avantaj yaratıyor.",
                "options": {
                    "A": {
                        "text": "Rakibin zayıflığını kullanın.",
                        "outcome": "Rekabet avantajı elde ettiniz.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_102"
                    },
                    "B": {
                        "text": "Lütfü Paşa'nın yokluğunda stratejik adımlar atın.",
                        "outcome": "Saraydaki nüfuzunuzu artırdınız.",
                        "score_changes": {"harem": 1, "suleyman": 2, "divan": 0},
                        "next_scene": "bolum_102"
                    },
                    "C": {
                        "text": "Durumu kendi çıkarınız doğrultusunda yönetin.",
                        "outcome": "Pragmatik bir tutum benimsediniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_102"
                    }
                }
            },
            "bolum_102": {
                "description": "Bolum 102: Şehzade Selim'in iyileşeceği umudu ve Cihangir'in üzüntüsüyle Hürrem'in kaybolma durumu gündemdedir.",
                "options": {
                    "A": {
                        "text": "Selim'in sağlığına odaklanın.",
                        "outcome": "Gelecek için umutlarınızı güçlendirdiniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_103"
                    },
                    "B": {
                        "text": "Kendi kaybolma riskinizi minimize edin.",
                        "outcome": "Kendinizi yeniden konumlandırdınız.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_103"
                    },
                    "C": {
                        "text": "Her iki durumu da dengeleyin.",
                        "outcome": "Karma strateji benimsediniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_103"
                    }
                }
            },
            "bolum_103": {
                "description": "Bolum 103: Hürrem'in yokluğu üzerine 'karanlığa düşmüşse asıl kaynağa bakmak icap eder' ifadesi vurgulanıyor.",
                "options": {
                    "A": {
                        "text": "Yokluğunuzun etkisini değerlendirin.",
                        "outcome": "Yokluğun yarattığı boşluğu analiz ettiniz.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_104"
                    },
                    "B": {
                        "text": "İşlerin seyrini kendi lehine çevirmeye çalışın.",
                        "outcome": "Gizli operasyonlarla müdahalede bulundunuz.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_104"
                    },
                    "C": {
                        "text": "Hiç müdahale etmeyin.",
                        "outcome": "Durumu pasif şekilde gözlemlediniz.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_104"
                    }
                }
            },
            "bolum_104": {
                "description": "Bolum 104: 'Elimden geldiğince size layık bir evlat olmaya çalışıyorum' ifadesiyle evlatların geleceği sorgulanıyor.",
                "options": {
                    "A": {
                        "text": "Evlatlar için stratejik planlar yapın.",
                        "outcome": "Çocuklarınızın geleceğini güvence altına almaya çalıştınız.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_105"
                    },
                    "B": {
                        "text": "Durumu kendi çıkarınız doğrultusunda kullanın.",
                        "outcome": "Kendi çıkarlarınızı maksimize etmek için strateji geliştirdiniz.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_105"
                    },
                    "C": {
                        "text": "Ebeveynlik etkisini sorgulayın.",
                        "outcome": "Çatışmalı duygular yaşadınız.",
                        "score_changes": {"harem": -1, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_105"
                    }
                }
            },
            "bolum_105": {
                "description": "Bolum 105: Şehzade Mustafa'nın gelişi ve 'İnanamıyorum onca vakit boşuna uğraştık' ifadesiyle işler değişiyor.",
                "options": {
                    "A": {
                        "text": "Gücünüzü korumak için planlarınızı gözden geçirin.",
                        "outcome": "Mevcut stratejilerinizi revize ettiniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_106"
                    },
                    "B": {
                        "text": "Mustafa'nın gelişiyle değişen dengeleri değerlendirin.",
                        "outcome": "Saraydaki güç dengesini analiz ettiniz.",
                        "score_changes": {"harem": 1, "suleyman": 2, "divan": 0},
                        "next_scene": "bolum_106"
                    },
                    "C": {
                        "text": "Her iki durumu da dikkate alarak hareket edin.",
                        "outcome": "Karma strateji benimsediniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_106"
                    }
                }
            },
            "bolum_106": {
                "description": "Bolum 106: Önemli işlerin olduğu bir dönemde, Gönül meselelerine odaklanılıyor.",
                "options": {
                    "A": {
                        "text": "Gönül eylemekten ziyade öncelikli meselelerle ilgilenin.",
                        "outcome": "Önemli konulara odaklanarak stratejik hamleler yaptınız.",
                        "score_changes": {"harem": 0, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_107"
                    },
                    "B": {
                        "text": "Gönül eylemi üzerinde de çalışın, ama diğer konuları göz ardı etmeyin.",
                        "outcome": "Her iki alanı da dengeleyerek hareket ettiniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_107"
                    },
                    "C": {
                        "text": "Önceliği tamamen Gönül'e verin.",
                        "outcome": "Dikkatinizi dağıttınız, riskler arttı.",
                        "score_changes": {"harem": -1, "suleyman": -1, "divan": -1},
                        "next_scene": "bolum_107"
                    }
                }
            },
            "bolum_107": {
                "description": "Bolum 107: Şehzade Bayezid'in Kütahya'ya gitmek istememesi ve Atmaca'nın gelişiyle ilgili kararlar alınmalı.",
                "options": {
                    "A": {
                        "text": "Önceliklerinizi belirleyip Bayezid'in kararını etkilemeye çalışın.",
                        "outcome": "Stratejik adımlar atıp etkili oldunuz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_108"
                    },
                    "B": {
                        "text": "Her iki durumu da dengeleyin.",
                        "outcome": "Karma strateji benimsediniz, dengede kalmaya çalıştınız.",
                        "score_changes": {"harem": 0, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_108"
                    },
                    "C": {
                        "text": "Sadece Bayezid'in kararlarına odaklanın.",
                        "outcome": "Tek taraflı strateji risk oluşturdu.",
                        "score_changes": {"harem": -1, "suleyman": -1, "divan": 0},
                        "next_scene": "bolum_108"
                    }
                }
            },
            "bolum_108": {
                "description": "Bolum 108: Evlilik ve Kapudan Paşa'nın kızı konusu gündemde. Evlilikler, ittifaklar ve politik araçlar olarak değerlendiriliyor.",
                "options": {
                    "A": {
                        "text": "İttifakları değerlendirin.",
                        "outcome": "Stratejik ittifaklar kurarak avantaj sağladınız.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "bolum_109"
                    },
                    "B": {
                        "text": "Evlilikleri politik araç olarak kullanın.",
                        "outcome": "Çıkar ilişkilerinizi güçlendirdiniz.",
                        "score_changes": {"harem": 2, "suleyman": 0, "divan": 1},
                        "next_scene": "bolum_109"
                    },
                    "C": {
                        "text": "Her iki stratejiyi de uygulayın.",
                        "outcome": "Karma strateji benimsediniz, risk ve avantajlar beraberinde geldi.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_109"
                    }
                }
            },
            "bolum_109": {
                "description": "Bolum 109: Hakikat, ateş, derya kavramları üzerine derin düşünceler; Mustafa Paşa'dan intikam arzusu ve aile bağları tartışılıyor.",
                "options": {
                    "A": {
                        "text": "Hakikati arayın.",
                        "outcome": "Derin düşüncelerle gerçekleri sorguladınız.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 1},
                        "next_scene": "bolum_110"
                    },
                    "B": {
                        "text": "İntikam duygunuzu analiz edin.",
                        "outcome": "İntikam arzunuzu değerlendirdiniz.",
                        "score_changes": {"harem": 1, "suleyman": 0, "divan": 0},
                        "next_scene": "bolum_110"
                    },
                    "C": {
                        "text": "Dış ilişkileri yakından takip edin.",
                        "outcome": "Diplomatik ilişkileri güçlendirmeye çalıştınız.",
                        "score_changes": {"harem": 0, "suleyman": 2, "divan": 0},
                        "next_scene": "bolum_110"
                    }
                }
            },
            "bolum_110": {
                "description": "Bolum 110: Venedik balosu, dostluk ve cephe genişlemesi konusu; 'Hünkar böyle karar vermiş...' ifadesiyle Hürrem'in manipülatif yönü ortaya çıkıyor.",
                "options": {
                    "A": {
                        "text": "İtibarınızı koruyun.",
                        "outcome": "Hünkar'ın kararına destek vererek itibarınızı güçlendirdiniz.",
                        "score_changes": {"harem": 1, "suleyman": 1, "divan": 0},
                        "next_scene": "final"
                    },
                    "B": {
                        "text": "Oyun içinde oyun oynayın, planlarınızı devreye sokun.",
                        "outcome": "Kendi planlarınızı uygulayarak stratejik avantaj sağladınız.",
                        "score_changes": {"harem": 2, "suleyman": 1, "divan": 1},
                        "next_scene": "final"
                    },
                    "C": {
                        "text": "Etki alanınızı genişletin.",
                        "outcome": "Seferde yer alacak kişilerle ilişkilerinizi geliştirip etki alanınızı artırdınız.",
                        "score_changes": {"harem": 2, "suleyman": 2, "divan": 0},
                        "next_scene": "final"
                    }
                }
            },
            "final": {
                "description": "Oyun sona erdi. Hürrem Sultan'ın saraydaki yolculuğu tamamlandı. Geçmiş seçimlerinizin sonucu bu şekilde ortaya çıktı.",
                "options": {}
            }
        }

            
 
# --- CHARACTER DATA ---
characters = [
    {
        "name": "Süleyman",
        "img": "images/sultan.png",
        "sound": "sounds/diger.mp3"
    },
    {
        "name": "Pargalı",
        "img": "images/pargali.png", 
        "sound": "sounds/diger.mp3"
    },
    {
        "name": "Hürrem",
        "img": "images/hurrem.png",
        "sound": "sounds/hurrem.mp3"
    }
]

# --- SCREEN FUNCTIONS ---

def render_character_selection():
    """Render character selection screen with improved mobile UX"""
    st.markdown('<div class="game-header"><h1 class="game-title">🏰 Osmanlı Sarayı Oyunu</h1></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="parchment"><h2 style="text-align: center; margin-top: 0;">Karakterini Seç</h2></div>', unsafe_allow_html=True)
    
    # Character selection with visual display
    char_html = '<div class="character-grid">'
    for char in characters:
        img_path = get_valid_path(char["img"])
        selected_class = "selected" if st.session_state.selected_character == char["name"] else ""
        char_html += f'''
        <div class="character-card {selected_class}">
            <img src="{img_path}" class="char-img" alt="{char["name"]}"/>
            <p class="char-name">{char["name"]}</p>
        </div>
        '''
    char_html += '</div>'
    
    st.markdown(char_html, unsafe_allow_html=True)
    
    # Character selection buttons
    st.markdown('<div class="parchment"><h3 style="text-align: center;">Karakterini seç:</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👑 Süleyman", key="select_suleyman", use_container_width=True):
            st.session_state.selected_character = "Süleyman"
            st.rerun()
    
    with col2:
        if st.button("⚔️ Pargalı", key="select_pargali", use_container_width=True):
            st.session_state.selected_character = "Pargalı"
            st.rerun()
    
    with col3:
        if st.button("🌹 Hürrem", key="select_hurrem", use_container_width=True):
            st.session_state.selected_character = "Hürrem"
            st.rerun()
    
    # Show selected character and confirm button
    if st.session_state.selected_character:
        st.markdown(f'<div class="parchment" style="text-align: center; background: linear-gradient(145deg, #98FB98, #90EE90);"><h3>✅ Seçilen Karakter: {st.session_state.selected_character}</h3></div>', unsafe_allow_html=True)
        
        if st.button("🎮 Oyunu Başlat", key="confirm_character", use_container_width=True):
            st.session_state.character_confirmed = True
            st.session_state.current_screen = "loading"
            # Play character sound
            char = next(c for c in characters if c["name"] == st.session_state.selected_character)
            play_audio_with_user_interaction(char["sound"], "character-sound")
            st.session_state.audio_played["character"] = True
            st.rerun()

def render_loading_screen():
    """Render loading screen with audio sequence"""
    st.markdown('<div class="loading-screen">', unsafe_allow_html=True)
    st.markdown(f'<div class="loading-text">🎭 {st.session_state.selected_character} olarak oyuna hazırlanıyorsun...</div>', unsafe_allow_html=True)
    
    # Play start sound after character sound
    if st.session_state.audio_played["character"] and not st.session_state.audio_played["start"]:
        play_audio_with_user_interaction("sounds/start.mp3", "start-sound")
        st.session_state.audio_played["start"] = True
    
    # Auto-progress to game after sounds
    if st.button("🚀 Oyuna Geç", key="start_game", use_container_width=True):
        st.session_state.current_screen = "game"
        if not st.session_state.audio_played["background"]:
            play_background_music()
            st.session_state.audio_played["background"] = True
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_game_screen():
    """Render main game screen"""
    st.markdown('<div class="game-header"><h1 class="game-title">🏰 Sarayda Bir Yolculuk</h1></div>', unsafe_allow_html=True)
    
    # Start background music if not already playing
    if not st.session_state.audio_played["background"]:
        play_background_music()
        st.session_state.audio_played["background"] = True
    
    # Display scores
    scores = st.session_state.game_data["scores"]
    score_html = f'''
    <div class="score-display">
        <div class="score-item">👥 Harem: {scores["harem"]}</div>
        <div class="score-item">👑 Süleyman: {scores["suleyman"]}</div>
        <div class="score-item">🏛️ Divan: {scores["divan"]}</div>
    </div>
    '''
    st.markdown(score_html, unsafe_allow_html=True)
    
    # Get current scene
    scene_key = st.session_state.game_data["current_scene"]
    scene = scenarios.get(scene_key)
    
    if not scene:
        render_game_end()
        return
    
    # Display scenario
    st.markdown(f'<div class="parchment"><strong>📜 Durum:</strong><br>{scene["description"]}</div>', unsafe_allow_html=True)
    
    # Display options
    st.markdown('<div class="parchment"><strong>🤔 Ne yapacaksın?</strong></div>', unsafe_allow_html=True)
    
    options = scene.get("options", {})
    
    # Option selection
    for key, option in options.items():
        button_key = f"option_{scene_key}_{key}"
        if st.button(f"{key}. {option['text']}", key=button_key, use_container_width=True):
            st.session_state.selected_option = key
            process_choice(scene_key, key, option)
            st.rerun()

def process_choice(scene_key, choice_key, choice_data):
    """Process the player's choice and update game state"""
    # Add to history
    st.session_state.game_data["history"].append({
        "scene": scene_key,
        "choice": choice_key,
        "outcome": choice_data["outcome"]
    })
    
    # Update scores
    for score_type, change in choice_data["score_changes"].items():
        st.session_state.game_data["scores"][score_type] += change
    
    # Calculate total score change to determine audio feedback
    total_score_change = sum(choice_data["score_changes"].values())
    
    # Play appropriate sound effect
    if total_score_change > 2:
        play_audio_with_user_interaction("sounds/dogrukarar.mp3", "correct-choice")
    else:
        play_audio_with_user_interaction("sounds/dikkat.mp3", "wrong-choice")
    
    # Move to next scene
    st.session_state.game_data["current_scene"] = choice_data["next_scene"]
    st.session_state.selected_option = None

def render_game_end():
    """Render game end screen with final scores"""
    st.markdown('<div class="game-header"><h1 class="game-title">🎊 Oyun Tamamlandı!</h1></div>', unsafe_allow_html=True)
    
    scores = st.session_state.game_data["scores"]
    total_score = sum(scores.values())
    
    # Determine result based on highest score
    highest_score = max(scores.values())
    winning_category = [k for k, v in scores.items() if v == highest_score][0]
    
    result_messages = {
        "harem": "🌹 Haremde büyük bir güç oldun! Kadınların saygısını kazandın.",
        "suleyman": "👑 Sultan'ın gözdesiri oldun! Siyasi gücün arttı.",
        "divan": "🏛️ Devlet işlerinde etkili oldun! Divan'da söz sahibisin."
    }
    
    st.markdown(f'<div class="parchment" style="text-align: center;"><h2>🏆 Sonuç</h2><p>{result_messages[winning_category]}</p><h3>Toplam Puan: {total_score}</h3></div>', unsafe_allow_html=True)
    
    # Final score display
    score_html = f'''
    <div class="score-display">
        <div class="score-item">👥 Harem: {scores["harem"]}</div>
        <div class="score-item">👑 Süleyman: {scores["suleyman"]}</div>
        <div class="score-item">🏛️ Divan: {scores["divan"]}</div>
    </div>
    '''
    st.markdown(score_html, unsafe_allow_html=True)

# --- MAIN APP FLOW ---

def main():
    """Main application flow"""
    if st.session_state.current_screen == "character_select":
        render_character_selection()
    elif st.session_state.current_screen == "loading":
        render_loading_screen()
    elif st.session_state.current_screen == "game":
        render_game_screen()
    
    # Reset button (always available)
    if st.button("🔄 Oyunu Sıfırla", key="reset_game", help="Oyunu baştan başlat"):
        # Reset all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Run the app
if __name__ == "__main__":
    main()
    
    
    


# --- GAME SCENARIOS ---


# --- CHARACTER DATA ---
characters = [
    {
        "name": "Süleyman",
        "img": "images/sultan.png",
        "sound": "sounds/diger.mp3"
    },
    {
        "name": "Pargalı",
        "img": "images/pargali.png", 
        "sound": "sounds/diger.mp3"
    },
    {
        "name": "Hürrem",
        "img": "images/hurrem.png",
        "sound": "sounds/hurrem.mp3"
    }
]

# --- SCREEN FUNCTIONS ---

def render_character_selection():
    """Render character selection screen with improved mobile UX"""
    st.markdown('<div class="game-header"><h1 class="game-title">🏰 Osmanlı Sarayı Oyunu</h1></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="parchment"><h2 style="text-align: center; margin-top: 0;">Karakterini Seç</h2></div>', unsafe_allow_html=True)
    
    # Character selection with visual display
    char_html = '<div class="character-grid">'
    for char in characters:
        img_path = get_valid_path(char["img"])
        selected_class = "selected" if st.session_state.selected_character == char["name"] else ""
        char_html += f'''
        <div class="character-card {selected_class}">
            <img src="{img_path}" class="char-img" alt="{char["name"]}"/>
            <p class="char-name">{char["name"]}</p>
        </div>
        '''
    char_html += '</div>'
    
    st.markdown(char_html, unsafe_allow_html=True)
    
    # Character selection buttons
    st.markdown('<div class="parchment"><h3 style="text-align: center;">Karakterini seç:</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("👑 Süleyman", key="select_suleyman", use_container_width=True):
            st.session_state.selected_character = "Süleyman"
            st.rerun()
    
    with col2:
        if st.button("⚔️ Pargalı", key="select_pargali", use_container_width=True):
            st.session_state.selected_character = "Pargalı"
            st.rerun()
    
    with col3:
        if st.button("🌹 Hürrem", key="select_hurrem", use_container_width=True):
            st.session_state.selected_character = "Hürrem"
            st.rerun()
    
    # Show selected character and confirm button
    if st.session_state.selected_character:
        st.markdown(f'<div class="parchment" style="text-align: center; background: linear-gradient(145deg, #98FB98, #90EE90);"><h3>✅ Seçilen Karakter: {st.session_state.selected_character}</h3></div>', unsafe_allow_html=True)
        
        if st.button("🎮 Oyunu Başlat", key="confirm_character", use_container_width=True):
            st.session_state.character_confirmed = True
            st.session_state.current_screen = "loading"
            # Play character sound
            char = next(c for c in characters if c["name"] == st.session_state.selected_character)
            play_audio_with_user_interaction(char["sound"], "character-sound")
            st.session_state.audio_played["character"] = True
            st.rerun()

def render_loading_screen():
    """Render loading screen with audio sequence"""
    st.markdown('<div class="loading-screen">', unsafe_allow_html=True)
    st.markdown(f'<div class="loading-text">🎭 {st.session_state.selected_character} olarak oyuna hazırlanıyorsun...</div>', unsafe_allow_html=True)
    
    # Play start sound after character sound
    if st.session_state.audio_played["character"] and not st.session_state.audio_played["start"]:
        play_audio_with_user_interaction("sounds/start.mp3", "start-sound")
        st.session_state.audio_played["start"] = True
    
    # Auto-progress to game after sounds
    if st.button("🚀 Oyuna Geç", key="start_game", use_container_width=True):
        st.session_state.current_screen = "game"
        if not st.session_state.audio_played["background"]:
            play_background_music()
            st.session_state.audio_played["background"] = True
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_game_screen():
    """Render main game screen"""
    st.markdown('<div class="game-header"><h1 class="game-title">🏰 Sarayda Bir Yolculuk</h1></div>', unsafe_allow_html=True)
    
    # Start background music if not already playing
    if not st.session_state.audio_played["background"]:
        play_background_music()
        st.session_state.audio_played["background"] = True
    
    # Display scores
    scores = st.session_state.game_data["scores"]
    score_html = f'''
    <div class="score-display">
        <div class="score-item">👥 Harem: {scores["harem"]}</div>
        <div class="score-item">👑 Süleyman: {scores["suleyman"]}</div>
        <div class="score-item">🏛️ Divan: {scores["divan"]}</div>
    </div>
    '''
    st.markdown(score_html, unsafe_allow_html=True)
    
    # Get current scene
    scene_key = st.session_state.game_data["current_scene"]
    scene = scenarios.get(scene_key)
    
    if not scene:
        render_game_end()
        return
    
    # Display scenario
    st.markdown(f'<div class="parchment"><strong>📜 Durum:</strong><br>{scene["description"]}</div>', unsafe_allow_html=True)
    
    # Display options
    st.markdown('<div class="parchment"><strong>🤔 Ne yapacaksın?</strong></div>', unsafe_allow_html=True)
    
    options = scene.get("options", {})
    
    # Option selection
    for key, option in options.items():
        button_key = f"option_{scene_key}_{key}"
        if st.button(f"{key}. {option['text']}", key=button_key, use_container_width=True):
            st.session_state.selected_option = key
            process_choice(scene_key, key, option)
            st.rerun()

def process_choice(scene_key, choice_key, choice_data):
    """Process the player's choice and update game state"""
    # Add to history
    st.session_state.game_data["history"].append({
        "scene": scene_key,
        "choice": choice_key,
        "outcome": choice_data["outcome"]
    })
    
    # Update scores
    for score_type, change in choice_data["score_changes"].items():
        st.session_state.game_data["scores"][score_type] += change
    
    # Calculate total score change to determine audio feedback
    total_score_change = sum(choice_data["score_changes"].values())
    
    # Play appropriate sound effect
    if total_score_change > 2:
        play_audio_with_user_interaction("sounds/dogrukarar.mp3", "correct-choice")
    else:
        play_audio_with_user_interaction("sounds/dikkat.mp3", "wrong-choice")
    
    # Move to next scene
    st.session_state.game_data["current_scene"] = choice_data["next_scene"]
    st.session_state.selected_option = None

def render_game_end():
    """Render game end screen with final scores"""
    st.markdown('<div class="game-header"><h1 class="game-title">🎊 Oyun Tamamlandı!</h1></div>', unsafe_allow_html=True)
    
    scores = st.session_state.game_data["scores"]
    total_score = sum(scores.values())
    
    # Determine result based on highest score
    highest_score = max(scores.values())
    winning_category = [k for k, v in scores.items() if v == highest_score][0]
    
    result_messages = {
        "harem": "🌹 Haremde büyük bir güç oldun! Kadınların saygısını kazandın.",
        "suleyman": "👑 Sultan'ın gözdesiri oldun! Siyasi gücün arttı.",
        "divan": "🏛️ Devlet işlerinde etkili oldun! Divan'da söz sahibisin."
    }
    
    st.markdown(f'<div class="parchment" style="text-align: center;"><h2>🏆 Sonuç</h2><p>{result_messages[winning_category]}</p><h3>Toplam Puan: {total_score}</h3></div>', unsafe_allow_html=True)
    
    # Final score display
    score_html = f'''
    <div class="score-display">
        <div class="score-item">👥 Harem: {scores["harem"]}</div>
        <div class="score-item">👑 Süleyman: {scores["suleyman"]}</div>
        <div class="score-item">🏛️ Divan: {scores["divan"]}</div>
    </div>
    '''
    st.markdown(score_html, unsafe_allow_html=True)

# --- MAIN APP FLOW ---

def main():
    """Main application flow"""
    if st.session_state.current_screen == "character_select":
        render_character_selection()
    elif st.session_state.current_screen == "loading":
        render_loading_screen()
    elif st.session_state.current_screen == "game":
        render_game_screen()
    
    # Reset button (always available)
    if st.button("🔄 Oyunu Sıfırla", key="reset_game", help="Oyunu baştan başlat"):
        # Reset all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Run the app
if __name__ == "__main__":
    main()