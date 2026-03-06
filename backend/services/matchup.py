from typing import Dict, Any, List
from services.analytics import AnalyticsService

class MatchupService:
    """
    Oyuncunun rakibiyle (Matchup) ne kadar avantajlı olduğunu analiz edip,
    A+, A, B, C, D, F gibi "Matchup Grade" hesaplar.
    """

    @classmethod
    def calculate_matchup_grade(
        cls, 
        player_avg_stats: float, 
        vegas_line: float, 
        l5_hit_rate: float, 
        opponent_defensive_rating: int, # Varsayılan: 1 (En iyi) - 30 (En kötü)
        head_to_head_avg: float
    ) -> Dict[str, Any]:
        """
        Gelen parametrelere göre maç puanını (100 üzerinden) bulup Harf Notuna çevirir.
        
        Kriter Ağırlıkları:
        - Recent Form (L5 Hit Rate): %35
        - Player Avg vs Vegas Line Farkı: %25
        - Head-to-Head Geçmişi vs Vegas Line: %20
        - Rakip Savunma Durumu (Opponent DEF rating): %20
        """
        score = 0.0

        # 1. L5 Hit Rate Puanı (%35 max)
        # Örn: %80 hit_rate = 80 * 0.35 = 28 puan
        l5_score = (l5_hit_rate / 100.0) * 35.0
        score += l5_score

        # 2. Player Avg vs Line (%25 max)
        # Oyuncu ortalaması çizgiden ne kadar yüksek?
        if vegas_line > 0:
            diff_percentage = ((player_avg_stats - vegas_line) / vegas_line) * 100.0
            
            # Fark +%20 ise tam puan(25), değilse ölçekli
            if diff_percentage >= 20:
                avg_line_score = 25.0
            elif diff_percentage > 0:
                avg_line_score = (diff_percentage / 20.0) * 25.0
            elif diff_percentage > -10:
                avg_line_score = 10.0 # Çizginin hemen altında
            else:
                avg_line_score = 0.0
        else:
            avg_line_score = 15.0 # Varsayılan
        
        score += avg_line_score

        # 3. Head-to-Head vs Line (%20 max)
        if head_to_head_avg > 0 and vegas_line > 0:
            h2h_diff = head_to_head_avg - vegas_line
            if h2h_diff > 2:
                h2h_score = 20.0
            elif h2h_diff > 0:
                h2h_score = 15.0
            elif h2h_diff > -2:
                h2h_score = 8.0
            else:
                h2h_score = 0.0
        else:
            h2h_score = 10.0 # Geçmiş yoksa nötr

        score += h2h_score

        # 4. Rakip Savunma (DEF Rating, 1-30. 30 en kötü savunma, yani over için iyi)
        # 30. Sıradaki takıma karşı tam puan (20)
        # 1. Sıradaki takıma karşı 0 puan
        # Formül: ((Rating - 1) / 29) * 20
        if 1 <= opponent_defensive_rating <= 30:
            def_score = ((opponent_defensive_rating - 1) / 29.0) * 20.0
        else:
            def_score = 10.0 # Bilinmiyorsa nötr
            
        score += def_score

        # Sonuç Yuvarlama (0 - 100 arası)
        final_score = min(max(round(score), 0), 100)
        
        # Harf notuna çeviri
        grade = cls._get_grade_letter(final_score)

        return {
            "score": final_score,
            "grade": grade,
            "breakdown": {
                "l5_score": round(l5_score, 1),
                "avg_vs_line_score": round(avg_line_score, 1),
                "h2h_score": round(h2h_score, 1),
                "def_rating_score": round(def_score, 1)
            }
        }

    @staticmethod
    def _get_grade_letter(score: int) -> str:
        """100'lük skoru A+ - F not sistemine dönüştürür."""
        if score >= 85:
            return "A+"
        elif score >= 75:
            return "A"
        elif score >= 65:
            return "B"
        elif score >= 55:
            return "C"
        elif score >= 40:
            return "D"
        else:
            return "F"

matchup_service = MatchupService()
