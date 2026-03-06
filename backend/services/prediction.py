import math
from typing import Dict, Any, List
from models.player_stats import PlayerStat
from services.analytics import AnalyticsService

class PredictionService:
    """
    Oyuncunun mevcut istatistik varyansına (standart sapma) ve ortalamasına,
    Aynı zamanda Vegas bahis oranlarına göre "Expected Value (EV)" ve "Hit Olasılığı" hesaplar.
    """

    @classmethod
    def calculate_prediction(cls, stats: List[PlayerStat], market: str, line: float, over_odds: int) -> Dict[str, Any]:
        """
        Hit Olasılığı ve EV (Beklenen Değer) hesaplar.
        
        * Not: İstatistik dizisinin boş olmaması gerekir.
        """
        if not stats:
             return {
                "hit_probability": 0.0,
                "expected_value": 0.0,
                "implied_probability": 0.0,
                "confidence_score": 0.0,
                "edge": 0.0
            }

        # 1. Oyuncunun istatistiksel ortalaması ve standart sapması (Varyans)
        values = [AnalyticsService._get_stat_value_for_market(s, market) for s in stats]
        mean = sum(values) / len(values)
        
        # Standart sapma hesaplama (stdev)
        variance = sum([((x - mean) ** 2) for x in values]) / len(values)
        std_dev = math.sqrt(variance) if variance > 0 else 0.5 # Sıfıra bölünme hatasını engelle

        # 2. Hit Probability (Normal Dağılım Kümülatif Fonksiyonu - CDF)
        # Oyuncunun ortalaması ve sapması ile 'line' değerini geçme ihtimalini hesaplar
        # = 1 - CDF(line)
        z_score = (line - mean) / std_dev
        
        # Math.erf (hata fonksiyonu) ile CDF
        cdf = 0.5 * (1 + math.erf(z_score / math.sqrt(2)))
        hit_probability = (1 - cdf) * 100.0 # Yüzde cinsinden Over ihtimali

        # 3. Vegas Oranından (American Odds) "Zımni (Implied) Olasılık" çıkarımı
        implied_prob = cls.american_odds_to_implied_probability(over_odds)

        # Edge (Avantaj): Gerçek olasılık, Vegas'ın biçtiği olasılıktan yüksekse avantajımız var demektir
        edge = hit_probability - implied_prob

        # 4. Expected Value (EV) Hesaplaması (100$ bahis üzerinden dönüş beklentisi)
        ev = cls.calculate_ev(hit_probability_percent=hit_probability, american_odds=over_odds, wager=100.0)

        # 5. Güven Skoru (Örneklem büyüklüğü ve std_dev'in düşüklüğüne göre)
        # Çok dalgalanan (yüksek std_dev) oyuncuya güven düşer. İstikrarlı oyuncuya güven artar.
        cv = std_dev / mean if mean > 0 else 1.0 # Coefficient of variation
        
        sample_size_multiplier = min(len(stats) / 20.0, 1.0) # Maksimum güven 20 maçlık veride elde edilir
        stability_score = max(0, 100 - (cv * 100)) # Varyasyon % si kadar güvenden düş
        
        confidence_score = (stability_score * 0.7) + (sample_size_multiplier * 30) # %70 istikrar, %30 veri büyüklüğü

        return {
            "hit_probability": round(hit_probability, 1), # % cinsinden
            "expected_value": round(ev, 2), # % veya $ cinsinden dönüş
            "implied_probability": round(implied_prob, 1),
            "confidence_score": round(confidence_score, 1),
            "edge": round(edge, 1),
            "mean": round(mean, 2),
            "std_dev": round(std_dev, 2)
        }

    @staticmethod
    def american_odds_to_implied_probability(odds: int) -> float:
        """American formattaki oranları (örn: -110 veya +120) % Olasılığa çevirir."""
        if odds == 0:
            return 50.0  # Oran yoksa %50
            
        if odds < 0:
            prob = (abs(odds) / (abs(odds) + 100)) * 100.0
        else:
            prob = (100 / (odds + 100)) * 100.0
            
        return round(prob, 2)

    @classmethod
    def calculate_ev(cls, hit_probability_percent: float, american_odds: int, wager: float = 100.0) -> float:
        """
        Girdiğiniz miktara göre (+100$) ne kadar kazanıp/kaybedeceğinizi hesaplar (Expected Value).
        Formül: (Kazanma İhtimali * Kazanç Tutarı) - (Kaybetme İhtimali * Bahis Tutarı)
        """
        prob_win = hit_probability_percent / 100.0
        prob_lose = 1.0 - prob_win

        if american_odds < 0:
            potential_profit = wager * (100.0 / abs(american_odds))
        else:
            potential_profit = wager * (american_odds / 100.0)

        ev = (prob_win * potential_profit) - (prob_lose * wager)
        return ev

prediction_service = PredictionService()
