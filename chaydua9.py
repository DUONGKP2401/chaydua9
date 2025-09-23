import hashlib
from collections import Counter, deque
import statistics
import platform
from datetime import datetime
import base64
import urllib.parse
import requests
import random
import string
import math
import json
import os
import time
from colorama import Fore, Style, init
init(autoreset=True)

NV = {
    1: '⚔️ Bậc thầy tấn công',
    2: '👊 Quyền sắt',
    3: '🤿 Thợ lặn sâu',
    4: '⚽ Cơn lốc sân cỏ',
    5: '🏇 Hiệp sĩ phi nhanh',
    6: '⚾ Vua home run'
}

class SmartAI:
    """
    🧠 HỆ THỐNG AI NÂNG CẤP v11.0 🧠
    50 logic phân tích nâng cao, lựa chọn duy nhất theo user & mã kì.
    """
    
    def __init__(self):
        self.total_logics = 50
        self.current_logic_index = -1
        self.selection_history = deque(maxlen=10)
        self.result_history = deque(maxlen=30)
        
        # --- 50 LOGIC NÂNG CẤP HOÀN TOÀN MỚI ---
        self.logics = [
            # --- Nhóm 1: Phân tích thống kê & xác suất (10 logic) ---
            self.logic_1_z_score_outlier, self.logic_2_poisson_distribution, self.logic_3_markov_chain_avoidance,
            self.logic_4_bayesian_inference_update, self.logic_5_standard_deviation_instability, self.logic_6_entropy_minimization,
            self.logic_7_chi_squared_test, self.logic_8_benford_law_deviation, self.logic_9_pareto_principle_focus,
            self.logic_10_monte_carlo_simulation,

            # --- Nhóm 2: Phân tích chuỗi & mẫu hình phức tạp (10 logic) ---
            self.logic_11_run_length_entropy, self.logic_12_fibonacci_sequence_skip, self.logic_13_prime_number_positioning,
            self.logic_14_adjacent_pair_avoidance, self.logic_15_reflection_pattern_break, self.logic_16_cycle_detection_floyd,
            self.logic_17_inter_win_interval_analysis, self.logic_18_duality_break_odd_even, self.logic_19_triad_inversion,
            self.logic_20_lexicographical_ordering_anomaly,

            # --- Nhóm 3: Lý thuyết trò chơi & Meta-Gaming (10 logic) ---
            self.logic_21_grimsby_gambit, self.logic_22_nash_equilibrium_assumption, self.logic_23_minimax_regret,
            self.logic_24_level_k_thinking, self.logic_25_exploit_the_overdog, self.logic_26_contrarian_consensus,
            self.logic_27_chaos_theory_edge, self.logic_28_information_asymmetry_exploit, self.logic_29_signaling_game_imitation,
            self.logic_30_anti_herding_maneuver,

            # --- Nhóm 4: Logic thích ứng & dựa trên trạng thái (10 logic) ---
            self.logic_31_volatility_adaptive_choice, self.logic_32_win_loss_momentum_shift, self.logic_33_state_change_detector,
            self.logic_34_kalman_filter_prediction, self.logic_35_feedback_loop_correction, self.logic_36_logic_performance_meta_analysis,
            self.logic_37_self_similarity_avoidance, self.logic_38_recency_frequency_score, self.logic_39_game_phase_detection,
            self.logic_40_systematic_desensitization,

            # --- Nhóm 5: Logic sáng tạo & Heuristics (10 logic) ---
            self.logic_41_quantum_superposition_collapse, self.logic_42_swarm_intelligence_divergence, self.logic_43_knight_tour_heuristic,
            self.logic_44_golden_ratio_bias, self.logic_45_fractal_dimension_break, self.logic_46_information_gap_fill,
            self.logic_47_weighted_recency_drought, self.logic_48_relative_strength_index, self.logic_49_perfect_information_fallacy,
            self.logic_50_occam_razor_choice
        ]
        self.logic_performance = {i: {'wins': 0, 'total': 0, 'win_rate': 0.0} for i in range(self.total_logics)}

    def select_logic_deterministically(self, user_id, ma_ki):
        input_string = f"{user_id}-{ma_ki}"
        hash_object = hashlib.sha256(input_string.encode())
        hex_dig = hash_object.hexdigest()
        big_integer = int(hex_dig, 16)
        logic_index = big_integer % self.total_logics
        self.current_logic_index = logic_index
        return self.logics[logic_index]

    def add_result(self, selected, actual_winner):
        is_win = (selected != actual_winner)
        self.result_history.append({'selected': selected, 'winner': actual_winner, 'is_win': is_win, 'logic_used': self.current_logic_index})
        perf = self.logic_performance[self.current_logic_index]
        perf['total'] += 1
        if is_win:
            perf['wins'] += 1
        perf['win_rate'] = perf['wins'] / perf['total'] if perf['total'] > 0 else 0.0

    def check_anti_patterns(self, top10, top100):
        if len(self.selection_history) >= 3 and len(set(list(self.selection_history)[-3:])) == 1:
            char = list(self.selection_history)[-1]
            alternatives = self.get_safe_alternatives(top100, [char])
            return random.choice(alternatives), f"🛡️ ANTI-PATTERN (AI lặp lại {char})"
        if len(top10[1]) >= 3 and len(set(top10[1][:3])) == 1:
            char = top10[1][0]
            alternatives = self.get_safe_alternatives(top100, [char])
            return random.choice(alternatives), f"🛡️ ANTI-PATTERN (Game lặp lại {char})"
        return None, None

    def get_safe_alternatives(self, top100_data, avoid_list):
        try:
            win_counts = sorted([(i + 1, wins) for i, wins in enumerate(top100_data[1])], key=lambda x: x[1])
            safe_chars = [char for char, wins in win_counts if char not in avoid_list]
            return safe_chars if safe_chars else [i for i in range(1, 7) if i not in avoid_list]
        except:
            return [i for i in range(1, 7) if i not in avoid_list]

    def get_win_counts_100(self, top100): return {i + 1: wins for i, wins in enumerate(top100[1])}
    
    # --- NHÓM 1: THỐNG KÊ & XÁC SUẤT ---
    def logic_1_z_score_outlier(self, top10, top100):
        """1. Tránh Ngoại lệ Z-Score: Tránh NV có tần suất thắng bất thường nhất (cao hoặc thấp) trong 100 ván."""
        wins = top100[1]
        mean = statistics.mean(wins)
        stdev = statistics.stdev(wins) if len(wins) > 1 else 1
        if stdev == 0: return random.randint(1, 6)
        z_scores = {i+1: abs((wins[i] - mean) / stdev) for i in range(6)}
        avoid = max(z_scores, key=z_scores.get)
        return self.get_safe_alternatives(top100, [avoid])[0]

    def logic_2_poisson_distribution(self, top10, top100):
        """2. Phân phối Poisson: Chọn NV có số lần thắng 'quá hạn' nhất so với tỷ lệ trung bình."""
        lambda_val = sum(top100[1]) / 100.0  # Tỷ lệ thắng trung bình mỗi ván cho bất kỳ NV nào
        droughts = self._get_droughts(top10[1] + list(self.result_history)[::-1])
        expected_drought = -math.log(1 - (1/6)) / lambda_val if lambda_val > 0 else 99
        deviations = {char: abs(drought - expected_drought) for char, drought in droughts.items()}
        return max(deviations, key=deviations.get)

    def logic_3_markov_chain_avoidance(self, top10, top100):
        """3. Chuỗi Markov: Dựa trên ván thắng cuối, tránh NV có xác suất chuyển tiếp cao nhất."""
        last_winner = top10[1][0]
        transitions = Counter()
        history = [r['winner'] for r in self.result_history] + top10[1]
        for i in range(len(history) - 1):
            if history[i+1] == last_winner:
                transitions[history[i]] += 1
        if not transitions: return self.get_safe_alternatives(top100, [last_winner])[0]
        avoid = transitions.most_common(1)[0][0]
        return self.get_safe_alternatives(top100, [avoid])[0]

    def logic_4_bayesian_inference_update(self, top10, top100):
        """4. Suy luận Bayes: Cập nhật 'niềm tin' về NV yếu nhất dựa trên 10 ván gần nhất."""
        prior = {char: 1/6 for char in range(1, 7)}
        likelihood = {char: (1 - (top10[1].count(char) / 10)) for char in range(1, 7)}
        posterior = {char: prior[char] * likelihood[char] for char in range(1, 7)}
        return max(posterior, key=posterior.get)

    def logic_5_standard_deviation_instability(self, top10, top100):
        """5. Bất ổn độ lệch chuẩn: Chọn NV có lịch sử thắng ổn định và ít biến động nhất."""
        win_indices = {char: [i for i, w in enumerate(reversed(top10[1])) if w == char] for char in range(1, 7)}
        stdevs = {}
        for char, indices in win_indices.items():
            if len(indices) < 2:
                stdevs[char] = 99 # Phạt những con ít thắng
            else:
                intervals = [indices[i+1] - indices[i] for i in range(len(indices)-1)]
                stdevs[char] = statistics.stdev(intervals) if len(intervals) > 1 else 0
        return min(stdevs, key=stdevs.get)

    def logic_6_entropy_minimization(self, top10, top100):
        """6. Giảm thiểu Entropy: Chọn NV ít được mong đợi nhất để phá vỡ tính trật tự của hệ thống."""
        freq = Counter(top10[1])
        total = len(top10[1])
        probabilities = {i+1: freq.get(i+1, 0) / total for i in range(6)}
        return min(probabilities, key=probabilities.get)

    def logic_7_chi_squared_test(self, top10, top100):
        """7. Kiểm định Chi-squared: Tìm NV có tần suất thắng sai lệch nhất so với kỳ vọng."""
        observed = top100[1]
        expected_val = sum(observed) / 6
        if expected_val == 0: return random.randint(1, 6)
        chi_values = {i+1: ((observed[i] - expected_val)**2) / expected_val for i in range(6)}
        # Tránh con sai lệch nhất, có thể là quá mạnh hoặc quá yếu
        avoid = max(chi_values, key=chi_values.get)
        return self.get_safe_alternatives(top100, [avoid])[0]

    def logic_8_benford_law_deviation(self, top10, top100):
        """8. Lệch luật Benford: Tránh NV có số lần thắng có chữ số đầu sai lệch nhất so với luật Benford."""
        first_digits = Counter([int(str(w)[0]) for w in top100[1] if w > 0])
        benford_probs = {1: 0.301, 2: 0.176, 3: 0.125, 4: 0.097, 5: 0.079, 6: 0.067}
        deviations = {}
        for i in range(1, 7):
            observed_freq = first_digits.get(i, 0) / sum(first_digits.values()) if sum(first_digits.values()) > 0 else 0
            deviations[i] = abs(observed_freq - benford_probs[i])
        avoid = max(deviations, key=deviations.get)
        return self.get_safe_alternatives(top100, [avoid])[0]

    def logic_9_pareto_principle_focus(self, top10, top100):
        """9. Nguyên lý Pareto (80/20): Giả định 20% NV (1-2 NV) gây ra 80% chiến thắng, và tránh chúng."""
        sorted_wins = sorted(self.get_win_counts_100(top100).items(), key=lambda x: x[1], reverse=True)
        avoid = [sorted_wins[0][0]]
        if len(sorted_wins) > 1: avoid.append(sorted_wins[1][0])
        return self.get_safe_alternatives(top100, avoid)[0]

    def logic_10_monte_carlo_simulation(self, top10, top100):
        """10. Mô phỏng Monte Carlo: Chạy mô phỏng ngẫu nhiên dựa trên tần suất 100 ván để tìm NV ít có khả năng thắng nhất."""
        weights = top100[1]
        if sum(weights) == 0: return random.randint(1, 6)
        simulations = 1000
        results = random.choices(range(1, 7), weights=weights, k=simulations)
        counts = Counter(results)
        return min(counts, key=counts.get)

    # --- NHÓM 2: CHUỖI & MẪU HÌNH PHỨC TẠP ---
    def _get_droughts(self, history):
        droughts = {char: len(history) for char in range(1, 7)}
        for i, winner in enumerate(history):
            if winner in droughts and droughts[winner] == len(history):
                droughts[winner] = i
        return droughts

    def logic_11_run_length_entropy(self, top10, top100):
        """11. Entropy độ dài chuỗi: Chọn NV phá vỡ chuỗi lặp lại (run) nhàm chán nhất."""
        runs = []
        if not top10[1]: return random.randint(1, 6)
        current_run = 1
        for i in range(1, len(top10[1])):
            if top10[1][i] == top10[1][i-1]:
                current_run += 1
            else:
                runs.append(current_run)
                current_run = 1
        runs.append(current_run)
        if statistics.mean(runs) < 1.5: # Nếu hệ thống đang hỗn loạn
            return top10[1][0] # Đi theo xu hướng
        else: # Nếu hệ thống đang có chuỗi
            return self.get_safe_alternatives(top100, [top10[1][0]])[0] # Phá vỡ chuỗi

    def logic_12_fibonacci_sequence_skip(self, top10, top100):
        """12. Bỏ qua chuỗi Fibonacci: Nếu vị trí các lần thắng của NV tạo thành chuỗi Fibonacci, tránh nó."""
        fib = [1, 2, 3, 5, 8, 13]
        for char in range(1, 7):
            indices = [i for i, w in enumerate(top10[1]) if w == char]
            if len(indices) >= 3 and all(idx in fib for idx in indices):
                return self.get_safe_alternatives(top100, [char])[0]
        return self._get_droughts(top10[1])[max(self._get_droughts(top10[1]), key=self._get_droughts(top10[1]).get)]

    def logic_13_prime_number_positioning(self, top10, top100):
        """13. Vị trí số nguyên tố: Tránh NV có xu hướng thắng ở các vị trí nguyên tố (2, 3, 5, 7)."""
        primes = {2, 3, 5, 7}
        prime_winners = [top10[1][i-1] for i in primes if i <= len(top10[1])]
        if not prime_winners: return random.randint(1, 6)
        counts = Counter(prime_winners)
        avoid = counts.most_common(1)[0][0]
        return self.get_safe_alternatives(top100, [avoid])[0]

    def logic_14_adjacent_pair_avoidance(self, top10, top100):
        """14. Tránh cặp liền kề: Tránh NV (N) nếu ván trước là (N-1) hoặc (N+1)."""
        last_winner = top10[1][0]
        avoid = [(last_winner % 6) + 1, (last_winner - 2 + 6) % 6 + 1]
        return self.get_safe_alternatives(top100, avoid)[0]

    def logic_15_reflection_pattern_break(self, top10, top100):
        """15. Phá vỡ mẫu phản chiếu: Nếu chuỗi có dạng ABC...CBA, tránh con tiếp theo trong mẫu."""
        history = top10[1]
        if len(history) >= 5 and history[:2] == list(reversed(history[2:4])):
             # A-B-C-B-A pattern
             return self.get_safe_alternatives(top100, [history[0]])[0]
        return self.logic_1_z_score_outlier(top10, top100) # fallback

    def logic_16_cycle_detection_floyd(self, top10, top100):
        """16. Phát hiện chu kỳ Floyd: Tìm chu kỳ trong lịch sử kết quả và tránh con tiếp theo."""
        history = [r['winner'] for r in self.result_history]
        if len(history) < 5: return random.randint(1, 6)
        tortoise = len(history) - 2
        hare = len(history) - 1
        while history[tortoise] != history[hare]:
            tortoise -= 1
            if tortoise < 0 or hare < 1: return random.randint(1,6)
        
        mu = 0
        tortoise = 0
        while history[tortoise] != history[hare]:
            tortoise += 1
            hare += 1
            mu += 1

        lam = 1
        hare = tortoise + 1
        while history[tortoise] != history[hare]:
            hare += 1
            lam += 1
        
        next_in_cycle_index = mu + (len(history) - mu) % lam
        avoid = history[next_in_cycle_index]
        return self.get_safe_alternatives(top100, [avoid])[0]

    def logic_17_inter_win_interval_analysis(self, top10, top100):
        """17. Phân tích khoảng cách thắng: Chọn NV có khoảng cách giữa các lần thắng gần đây nhất bất thường."""
        intervals = {}
        for char in range(1, 7):
            indices = [i for i, w in enumerate(top10[1]) if w == char]
            if len(indices) > 1:
                intervals[char] = indices[0] - indices[1] 
            else:
                intervals[char] = 99 # Phạt
        return max(intervals, key=intervals.get)

    def logic_18_duality_break_odd_even(self, top10, top100):
        """18. Phá vỡ lưỡng cực Chẵn/Lẻ: Nếu có chuỗi chẵn hoặc lẻ, chọn một NV từ nhóm đối diện."""
        parity_history = [w % 2 for w in top10[1][:5]]
        if len(set(parity_history)) == 1: # Chuỗi đồng nhất
            target_parity = 1 - parity_history[0]
            candidates = [c for c in range(1, 7) if c % 2 == target_parity]
            return random.choice(candidates)
        return self.logic_1_z_score_outlier(top10, top100)

    def logic_19_triad_inversion(self, top10, top100):
        """19. Đảo ngược bộ ba: Nếu mẫu là A->B->C, tránh con D sao cho (A,B,C,D) tạo thành một nhóm logic."""
        if len(top10[1]) < 3: return random.randint(1,6)
        a, b, c = top10[1][2], top10[1][1], top10[1][0]
        if a < b < c: # Chuỗi tăng
            candidates = [i for i in range(1,7) if i < c]
            return self.get_safe_alternatives(top100, candidates)[0]
        if a > b > c: # Chuỗi giảm
            candidates = [i for i in range(1,7) if i > c]
            return self.get_safe_alternatives(top100, candidates)[0]
        return self.logic_1_z_score_outlier(top10, top100)

    def logic_20_lexicographical_ordering_anomaly(self, top10, top100):
        """20. Dị thường thứ tự từ điển: Chọn NV ít xuất hiện nhất trong các cặp có thứ tự."""
        counts = Counter()
        history = top10[1]
        for i in range(len(history) - 1):
            pair = tuple(sorted((history[i], history[i+1])))
            counts[pair] += 1
        least_common_pair = counts.most_common()[-1][0]
        return random.choice(least_common_pair)

    # --- NHÓM 3: LÝ THUYẾT TRÒ CHƠI & META ---
    def logic_21_grimsby_gambit(self, top10, top100):
        """21. Gambit Grimsby: Chọn NV yếu nhất, nhưng chỉ khi nó không phải là NV yếu nhất rõ ràng."""
        sorted_chars = self.get_safe_alternatives(top100, [])
        if len(sorted_chars) > 1:
            return sorted_chars[1] # Chọn con yếu thứ hai
        return sorted_chars[0]

    def logic_22_nash_equilibrium_assumption(self, top10, top100):
        """22. Giả định cân bằng Nash: Giả sử các 'người chơi' khác đang tối ưu hóa, hãy chọn con ít được chọn nhất."""
        return self.logic_1_z_score_outlier(top10, top100) # Trong một game ngẫu nhiên, đây là lựa chọn hợp lý nhất

    def logic_23_minimax_regret(self, top10, top100):
        """23. Tiếc nuối tối thiểu: Chọn NV mà nếu nó thắng, sự 'tiếc nuối' (dựa trên tần suất) là thấp nhất."""
        wins = self.get_win_counts_100(top100)
        max_wins = max(wins.values())
        regret = {char: max_wins - win_count for char, win_count in wins.items()}
        return min(regret, key=regret.get)

    def logic_24_level_k_thinking(self, top10, top100):
        """24. Tư duy cấp K (K=2): 'Tôi nghĩ rằng bạn nghĩ rằng tôi sẽ chọn X, vì vậy tôi sẽ chọn Y'."""
        # K=0: Chọn ngẫu nhiên
        # K=1: Người chơi sẽ nghĩ AI chọn con yếu nhất (logic 1). 
        level1_choice = sorted(self.get_win_counts_100(top100).items(), key=lambda x:x[1])[0][0]
        # K=2: AI dự đoán người chơi sẽ cược vào con K=1, nên AI sẽ tránh nó.
        return self.get_safe_alternatives(top100, [level1_choice])[0]

    def logic_25_exploit_the_overdog(self, top10, top100):
        """25. Khai thác kẻ mạnh: Luôn đặt cược chống lại NV mạnh nhất trong 100 ván."""
        counts = self.get_win_counts_100(top100)
        strongest = max(counts, key=counts.get)
        return self.get_safe_alternatives(top100, [strongest])[0]

    def logic_26_contrarian_consensus(self, top10, top100):
        """26. Ngược số đông: Chạy 3 logic đơn giản và chọn con không được chúng chọn."""
        c1 = sorted(self.get_win_counts_100(top100).items(), key=lambda x:x[1])[0][0] # Yếu nhất 100
        c2 = sorted(Counter(top10[1]).items(), key=lambda x:x[1])[0][0] # Yếu nhất 10
        c3 = self._get_droughts(top10[1])[max(self._get_droughts(top10[1]), key=self._get_droughts(top10[1]).get)] # Trễ nhất
        consensus = {c1, c2, c3}
        return self.get_safe_alternatives(top100, list(consensus))[0]

    def logic_27_chaos_theory_edge(self, top10, top100):
        """27. Lợi thế Hỗn loạn: Nếu 10 ván gần đây có độ phân tán cao (nhiều người thắng khác nhau), hãy đi theo xu hướng gần nhất."""
        unique_winners_10 = len(set(top10[1]))
        if unique_winners_10 >= 5: # Hỗn loạn
            return top10[1][0] # Bắt chước người thắng cuối
        else: # Trật tự
            return self.get_safe_alternatives(top100, [top10[1][0]])[0] # Phá vỡ

    def logic_28_information_asymmetry_exploit(self, top10, top100):
        """28. Khai thác thông tin bất đối xứng: AI biết lịch sử cược của mình, người chơi thì không. Tránh lặp lại lựa chọn thua."""
        recent_losses = [r['selected'] for r in self.result_history if not r['is_win']][-3:]
        if recent_losses:
            return self.get_safe_alternatives(top100, recent_losses)[0]
        return self.logic_1_z_score_outlier(top10, top100)

    def logic_29_signaling_game_imitation(self, top10, top100):
        """29. Bắt chước trò chơi tín hiệu: Nếu 2 ván cuối là (X, Y), tìm lần cuối (X, Y) xuất hiện và tránh con theo sau nó."""
        if len(top10[1]) < 2: return random.randint(1, 6)
        p1, p2 = top10[1][1], top10[1][0]
        history = [r['winner'] for r in self.result_history]
        for i in range(len(history) - 2):
            if history[i] == p1 and history[i+1] == p2:
                return self.get_safe_alternatives(top100, [history[i+2]])[0]
        return self.get_safe_alternatives(top100, [p2])[0]

    def logic_30_anti_herding_maneuver(self, top10, top100):
        """30. Chống hiệu ứng bầy đàn: Tránh 3 NV thắng nhiều nhất trong 10 ván gần nhất."""
        counts10 = Counter(top10[1])
        avoid = [c[0] for c in counts10.most_common(3)]
        return self.get_safe_alternatives(top100, avoid)[0]

    # --- NHÓM 4: THÍCH ỨNG & DỰA TRÊN TRẠNG THÁI ---
    def logic_31_volatility_adaptive_choice(self, top10, top100):
        """31. Thích ứng biến động: Nếu hệ thống biến động (thắng thua thất thường), chọn an toàn. Nếu ổn định, chọn rủi ro."""
        win_rates = [p['win_rate'] for p in self.logic_performance.values() if p['total'] > 0]
        if not win_rates or statistics.stdev(win_rates) > 0.3: # Biến động
            return sorted(self.get_win_counts_100(top100).items(), key=lambda x:x[1])[0][0]
        else: # Ổn định
            return sorted(self.get_win_counts_100(top100).items(), key=lambda x:x[1], reverse=True)[0][0]

    def logic_32_win_loss_momentum_shift(self, top10, top100):
        """32. Chuyển đổi động lượng: Nếu AI đang thắng, tiếp tục logic cũ. Nếu thua, chuyển sang logic đối nghịch."""
        if not self.result_history: return self.logic_1_z_score_outlier(top10, top100)
        last_result = self.result_history[-1]
        if last_result['is_win']:
            return self.logics[last_result['logic_used']](top10, top100)
        else: # Thua, làm ngược lại
            last_choice = self.logics[last_result['logic_used']](top10, top100)
            return self.get_safe_alternatives(top100, [last_choice])[0]

    def logic_33_state_change_detector(self, top10, top100):
        """33. Dò trạng thái: So sánh phân phối 10 ván gần nhất với 10 ván trước đó. Nếu khác biệt lớn, hệ thống đã thay đổi."""
        if len(top10[1]) < 20:
             history = [r['winner'] for r in self.result_history]
        else:
             history = top10[1]

        if len(history) < 20: return random.randint(1,6)
        
        dist1 = Counter(history[:10])
        dist2 = Counter(history[10:20])
        diff = sum(abs(dist1.get(i,0) - dist2.get(i,0)) for i in range(1,7))
        if diff > 6: # Thay đổi lớn
            return self.logic_10_monte_carlo_simulation(top10,top100) # Reset, tin vào dài hạn
        else: # Ổn định
            return self.logic_27_chaos_theory_edge(top10,top100) # Tin vào ngắn hạn

    def logic_34_kalman_filter_prediction(self, top10, top100):
        """34. Dự đoán Kalman: Coi tần suất thắng là một tín hiệu nhiễu và lọc để tìm ra 'tần suất thật'."""
        # Simplified Kalman-like logic
        estimate = dict(self.get_win_counts_100(top100))
        for winner in top10[1]:
            for char in range(1, 7):
                if char == winner:
                    estimate[char] = estimate[char] * 0.9 + (1) * 0.1 # Cập nhật
                else:
                    estimate[char] = estimate[char] * 0.9 # Giảm dần
        return min(estimate, key=estimate.get)

    def logic_35_feedback_loop_correction(self, top10, top100):
        """35. Sửa lỗi vòng lặp: Nếu logic được chọn gần đây có tỷ lệ thắng thấp, hãy tránh nó và các logic tương tự."""
        last_5_logics = [r['logic_used'] for r in self.result_history][-5:]
        bad_logics = [l for l in last_5_logics if self.logic_performance[l]['win_rate'] < 0.4 and self.logic_performance[l]['total'] > 5]
        if not bad_logics: return self.logic_1_z_score_outlier(top10, top100)
        
        bad_group = bad_logics[0] // 10
        # Chuyển sang nhóm logic khác
        next_group = (bad_group + 1) % 5
        logic_idx = next_group * 10 + random.randint(0, 9)
        return self.logics[logic_idx](top10, top100)

    def logic_36_logic_performance_meta_analysis(self, top10, top100):
        """36. Phân tích meta logic: Chọn logic có hiệu suất tốt nhất trong 30 ván vừa qua."""
        best_perf = -1
        best_logic = 0
        for i in range(self.total_logics):
            perf = self.logic_performance[i]
            if perf['total'] > 5 and perf['win_rate'] > best_perf:
                best_perf = perf['win_rate']
                best_logic = i
        return self.logics[best_logic](top10, top100)
    
    def logic_37_self_similarity_avoidance(self, top10, top100):
        """37. Tránh Tự đồng dạng: AI sẽ tránh lặp lại một lựa chọn trong N ván gần nhất, bất kể thắng thua."""
        avoid = list(self.selection_history)
        if not avoid: return random.randint(1,6)
        return self.get_safe_alternatives(top100, avoid)[0]

    def logic_38_recency_frequency_score(self, top10, top100):
        """38. Điểm RF (Recency-Frequency): Chọn NV có điểm RF thấp nhất (thắng đã lâu và tần suất thấp)."""
        droughts = self._get_droughts(top10[1])
        freqs = self.get_win_counts_100(top100)
        # Normalize
        max_drought = max(droughts.values()) if droughts else 1
        max_freq = max(freqs.values()) if freqs else 1
        scores = {c: (droughts.get(c, max_drought) / max_drought) - (freqs.get(c, 0) / max_freq) for c in range(1, 7)}
        return max(scores, key=scores.get) # Điểm cao nhất là tốt nhất (trễ cao, tần suất thấp)

    def logic_39_game_phase_detection(self, top10, top100):
        """39. Nhận diện giai đoạn game: 'Đầu game' (dưới 20 ván) thì an toàn, 'giữa game' thì tấn công."""
        if len(self.result_history) < 20: # Đầu game
            return sorted(self.get_win_counts_100(top100).items(), key=lambda x:x[1])[0][0]
        else: # Giữa game
            return self._get_droughts(top10[1])[max(self._get_droughts(top10[1]), key=self._get_droughts(top10[1]).get)]

    def logic_40_systematic_desensitization(self, top10, top100):
        """40. Giải mẫn cảm có hệ thống: Chọn ngẫu nhiên từ 3 NV yếu nhất để làm AI khó bị dự đoán hơn."""
        candidates = self.get_safe_alternatives(top100, [])[:3]
        return random.choice(candidates)

    # --- NHÓM 5: SÁNG TẠO & HEURISTICS ---
    def logic_41_quantum_superposition_collapse(self, top10, top100):
        """41. Sụp đổ lượng tử: Coi tất cả NV yếu là một 'trạng thái chồng chập' và chọn ngẫu nhiên một."""
        return self.logic_40_systematic_desensitization(top10, top100)

    def logic_42_swarm_intelligence_divergence(self, top10, top100):
        """42. Phân kỳ bầy đàn: Nếu nhiều NV đang 'tụ lại' ở một mức thắng, chọn một con ở ngoài 'bầy'."""
        wins = sorted(top100[1])
        gaps = [wins[i+1] - wins[i] for i in range(len(wins)-1)]
        if not gaps: return random.randint(1,6)
        max_gap_index = gaps.index(max(gaps))
        # Chọn con nằm ở phía ít đông đúc hơn của khoảng trống lớn nhất
        if max_gap_index > len(wins) / 2:
            return top100[1].index(wins[-1]) + 1 # Con mạnh nhất
        else:
            return top100[1].index(wins[0]) + 1 # Con yếu nhất

    def logic_43_knight_tour_heuristic(self, top10, top100):
        """43. Heuristic Mã đi tuần: Coi NV là bàn cờ 2x3, di chuyển như quân mã từ vị trí thắng cuối."""
        board = {1:(0,0), 2:(0,1), 3:(0,2), 4:(1,0), 5:(1,1), 6:(1,2)}
        rev_board = {(0,0):1, (0,1):2, (0,2):3, (1,0):4, (1,1):5, (1,2):6}
        last_pos = board[top10[1][0]]
        moves = [(1,2), (1,-2), (-1,2), (-1,-2), (2,1), (2,-1), (-2,1), (-2,-1)]
        valid_moves = []
        for move in moves:
            new_pos = (last_pos[0] + move[0], last_pos[1] + move[1])
            if new_pos in rev_board:
                valid_moves.append(rev_board[new_pos])
        if not valid_moves: return self.get_safe_alternatives(top100, [top10[1][0]])[0]
        # Tránh một trong các nước đi hợp lệ
        return self.get_safe_alternatives(top100, valid_moves)[0]

    def logic_44_golden_ratio_bias(self, top10, top100):
        """44. Thiên vị Tỷ lệ vàng: Chọn NV có tỷ lệ thắng gần nhất với 1/phi (phi ~ 1.618)."""
        phi = 1.618
        target_ratio = 1/phi
        total_wins = sum(top100[1])
        if total_wins == 0: return random.randint(1,6)
        ratios = {i+1: top100[1][i] / total_wins for i in range(6)}
        closest = min(ratios, key=lambda c: abs(ratios[c] - target_ratio))
        return closest

    def logic_45_fractal_dimension_break(self, top10, top100):
        """45. Phá vỡ chiều Fractal: Nếu chuỗi kết quả có tính lặp lại ở các quy mô khác nhau, phá vỡ nó."""
        h5 = top10[1][:5]
        h10 = top10[1][:10]
        if len(h5) < 5 or len(h10) < 10: return random.randint(1,6)
        dist5 = Counter(h5)
        dist10 = Counter(h10)
        is_fractal = True
        for char in range(1,7):
            if dist10.get(char,0) > 0 and abs(dist5.get(char,0)*2 - dist10.get(char,0)) > 2:
                is_fractal = False
                break
        if is_fractal: # Nếu có tính fractal, tránh con phổ biến nhất
            return dist10.most_common(1)[0][0]
        return self.logic_1_z_score_outlier(top10, top100)
    
    def logic_46_information_gap_fill(self, top10, top100):
        """46. Lấp đầy khoảng trống thông tin: Chọn NV không thắng trong 10 ván gần nhất."""
        winners10 = set(top10[1])
        candidates = list(set(range(1, 7)) - winners10)
        if candidates:
            return random.choice(candidates)
        return sorted(Counter(top10[1]).items(), key=lambda x:x[1])[0][0]

    def logic_47_weighted_recency_drought(self, top10, top100):
        """47. Độ trễ gia quyền: Tính điểm 'trễ' bằng cách cộng các vị trí không thắng, chọn con có điểm cao nhất."""
        scores = {c: 0 for c in range(1, 7)}
        for i, winner in enumerate(reversed(top10[1])):
            for c in range(1, 7):
                if c != winner:
                    scores[c] += (10 - i) # Vị trí càng gần đây, điểm cộng càng cao
        return max(scores, key=scores.get)

    def logic_48_relative_strength_index(self, top10, top100):
        """48. Chỉ số sức mạnh tương đối (RSI): So sánh 'sức mạnh' của NV trong 10 ván so với 100 ván."""
        strength100 = {i+1: top100[1][i] / 100 for i in range(6)}
        strength10 = {i+1: top10[1].count(i+1) / 10 for i in range(6)}
        rsi = {c: strength10.get(c,0) / strength100.get(c,0.01) for c in range(1, 7)}
        # Tránh con đang 'quá mua' (RSI cao)
        overbought = max(rsi, key=rsi.get)
        return self.get_safe_alternatives(top100, [overbought])[0]

    def logic_49_perfect_information_fallacy(self, top10, top100):
        """49. Ngụy biện thông tin hoàn hảo: Hành động như thể thông tin trong 10 ván là 'hoàn hảo' và chọn con duy nhất chưa xuất hiện."""
        return self.logic_46_information_gap_fill(top10, top100)

    def logic_50_occam_razor_choice(self, top10, top100):
        """50. Lựa chọn Dao cạo Occam: Giải pháp đơn giản nhất là tốt nhất. Tránh người thắng cuối cùng."""
        last_winner = top10[1][0]
        return self.get_safe_alternatives(top100, [last_winner])[0]
        
    def analyze_and_select(self, top10_data, top100_data, user_id, ma_ki):
        try:
            selected, logic_name = self.check_anti_patterns(top10_data, top100_data)
            if selected:
                self.selection_history.append(selected)
                return selected, logic_name

            logic_function = self.select_logic_deterministically(user_id, ma_ki)
            selected = logic_function(top10_data, top100_data)
            
            if not isinstance(selected, int) or not (1 <= selected <= 6):
                selected = random.randint(1, 6)
            
            logic_name = logic_function.__doc__.strip() if logic_function.__doc__ else f"🧠 LOGIC_{self.current_logic_index + 1}"
            
            self.selection_history.append(selected)
            return selected, logic_name
        
        except Exception as e:
            # prints(255, 0, 0, f'❌ Lỗi AI: {e}') # Optional: to avoid screen clutter
            fallback = random.randint(1, 6)
            self.selection_history.append(fallback)
            return fallback, "🚨 CHẾ ĐỘ DỰ PHÒNG"

smart_ai = SmartAI()

def clear_screen():
    os.system('cls' if platform.system() == "Windows" else 'clear')

def prints(r, g, b, text="text", end="\n"):
    print("\033[38;2;{};{};{}m{}\033[0m".format(r, g, b, text), end=end)

def banner(game):
    banner_txt = """
████████╗██████╗ ██╗  ██╗
╚══██╔══╝██╔══██╗██║ ██╔╝
   ██║   ██████╔╝█████╔╝ 
   ██║   ██╔═══╝ ██╔═██╗ 
   ██║   ██║     ██║  ██╗
   ╚═╝   ╚═╝     ╚═╝  ╚═╝  
    """
    for i in banner_txt.split('\n'):
        x, y, z = 200, 255, 255
        for j in range(len(i)):
            prints(x, y, z, i[j], end='')
            x -= 4
            time.sleep(0.001)
        print()
    prints(247, 255, 97, "✨" + "═" * 45 + "✨")
    prints(32, 230, 151, "🌟 XWORLD AI - {} v11.0🌟".format(game).center(47))
    prints(247, 255, 97, "═" * 47)
    prints(255, 215, 0, "🧠 50 LOGIC NÂNG CAO & DUY NHẤT 🧠".center(47))
    prints(255, 100, 100, "🛡️ META-GAMING & LÝ THUYẾT TRÒ CHƠI 🛡️".center(47))
    prints(100, 255, 100, "🎯 CHỐNG BẮT BÀI & PHÂN TÍCH SÂU 🎯".center(47))
    prints(247, 255, 97, "═" * 47)
    prints(7, 205, 240, "📱 Telegram: tankeko12")
    prints(7, 205, 240, "👥 Nhóm Zalo: https://zalo.me/g/viiuml595")
    prints(7, 205, 240, "👨‍💼 Admin: Duong Phung | Zalo: 0865656488")
    prints(247, 255, 97, "═" * 47)

def load_data_cdtd():
    if os.path.exists('data-xw-cdtd.txt'):
        prints(0, 255, 243, 'Bạn có muốn sử dụng thông tin đã lưu hay không? (y/n): ', end='')
        x = input()
        if x.lower() == 'y':
            with open('data-xw-cdtd.txt', 'r', encoding='utf-8') as f:
                return json.load(f)
        prints(247, 255, 97, "═" * 47)
    guide = """
    Huướng dẫn lấy link:
    1.Truy cập vào trang web xworld.io
    2.Đăng nhập tải khoản của bạn
    3.Tìm và nhấn vào chạy đua tốc độ
    4. Nhấn lập tức truy cập
    5.Copy link trang web đó và dán vào đây
"""
    prints(218, 255, 125, guide)
    prints(247, 255, 97, "═" * 47)
    prints(125, 255, 168, '📋Nhập link của bạn:', end=' ')
    link = input()
    try:
        user_id = link.split('&')[0].split('?userId=')[1]
        user_secretkey = link.split('&')[1].split('secretKey=')[1]
    except IndexError:
        prints(255, 0, 0, "Link không hợp lệ, vui lòng thử lại!")
        return load_data_cdtd()
        
    prints(218, 255, 125, '    User id của bạn là {}'.format(user_id))
    prints(218, 255, 125, '    User secret key của bạn là {}'.format(user_secretkey))
    json_data = {
        'user-id': user_id,
        'user-secret-key': user_secretkey,
    }
    with open('data-xw-cdtd.txt', 'w+', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4, ensure_ascii=False)
    return json_data

def top_100_cdtd(s):
    headers = {
        'accept': '*/*', 'accept-language': 'vi,en;q=0.9', 'origin': 'https://sprintrun.win',
        'priority': 'u=1, i', 'referer': 'https://sprintrun.win/', 'user-agent': 'Mozilla/5.0',
    }
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_100_issues', headers=headers, timeout=10).json()
        nv = [1, 2, 3, 4, 5, 6]
        kq = [response['data']['athlete_2_win_times'][str(i)] for i in range(1, 7)]
        return nv, kq
    except Exception as e:
        prints(255, 0, 0, f'Lỗi khi lấy top 100: {e}, thử lại...')
        time.sleep(2)
        return top_100_cdtd(s)

def top_10_cdtd(s, headers):
    try:
        response = s.get('https://api.sprintrun.win/sprint/recent_10_issues', headers=headers, timeout=10).json()
        ki, kq = [], []
        for i in response['data']['recent_10']:
            ki.append(i['issue_id'])
            kq.append(i['result'][0])
        return ki, kq
    except Exception as e:
        prints(255, 0, 0, f'Lỗi khi lấy top 10: {e}, thử lại...')
        time.sleep(2)
        return top_10_cdtd(s, headers)

def print_data(data_top10_cdtd, data_top100_cdtd):
    prints(247, 255, 97, "═" * 47)
    prints(0, 255, 250, "📊 DỮ LIỆU 10 VÁN GẦN NHẤT:".center(50))
    for i in range(len(data_top10_cdtd[0])):
        prints(255, 255, 0, f'🏁 Kì {data_top10_cdtd[0][i]}: {NV[int(data_top10_cdtd[1][i])]}')
    prints(247, 255, 97, "═" * 47)
    prints(0, 255, 250, "📈 DỮ LIỆU 100 VÁN GẦN NHẤT:".center(50))
    for i in range(6):
        prints(255, 255, 0, f'🏆 {NV[int(i+1)]} về nhất {data_top100_cdtd[1][int(i)]} lần')
    prints(247, 255, 97, "═" * 47)

def selected_NV(data_top10_cdtd, data_top100_cdtd, htr, heso, bet_amount0, user_id, ma_ki):
    bet_amount = bet_amount0
    if len(htr) >= 1 and not htr[-1]['kq']:
        bet_amount = heso * htr[-1]['bet_amount']
    
    selected_char, logic_name = smart_ai.analyze_and_select(data_top10_cdtd, data_top100_cdtd, user_id, ma_ki)
    
    prints(0, 255, 200, f'⚡ {logic_name}')
    return selected_char, bet_amount

def kiem_tra_kq_cdtd(s, headers, kq_dat_cuoc, ki):
    start_time = time.time()
    if kq_dat_cuoc:
        prints(0, 255, 37, f'⏰ Đã cược TRÁNH {NV[kq_dat_cuoc]}, đang đợi kết quả kì #{ki}...')
    else:
        prints(0, 255, 37, f'⏰ Ván nghỉ, đang đợi kết quả kì #{ki}...')

    while True:
        if time.time() - start_time > 90:
            prints(255, 100, 0, f"\nLỖI: Không nhận được kết quả cho kì #{ki} sau 90 giây. Có thể do lỗi mạng hoặc API.")
            return None

        try:
            data_top10_moi = top_10_cdtd(s, headers)
            
            if int(data_top10_moi[0][0]) == int(ki):
                ket_qua_thuc_te = int(data_top10_moi[1][0])
                
                prints(0, 255, 30, f'\n🏆 KẾT QUẢ KÌ {ki} LÀ: {NV[ket_qua_thuc_te]}')
                
                if kq_dat_cuoc:
                    smart_ai.add_result(kq_dat_cuoc, ket_qua_thuc_te)
                    if ket_qua_thuc_te != kq_dat_cuoc:
                        prints(0, 255, 37, f'🎉 BẠN ĐÃ THẮNG! (Vì kết quả là {NV[ket_qua_thuc_te]}, không phải {NV[kq_dat_cuoc]})')
                        return True
                    else:
                        prints(255, 0, 0, f'😔 BẠN ĐÃ THUA. (Vì kết quả TRÙNG với nhân vật đã cược tránh là {NV[kq_dat_cuoc]})')
                        return False
                else:
                    return "PAUSED"
            
            elapsed = time.time() - start_time
            prints(0, 255, 197, f'⏳ Vẫn đang đợi kết quả kì #{ki}... {int(elapsed)}s', end='\r')
            time.sleep(2)

        except Exception as e:
            prints(255, 0, 0, f"\nLỗi trong lúc chờ kết quả: {e}. Thử lại sau 5 giây...")
            time.sleep(5)

def user_asset(s, headers):
    try:
        json_data = {'user_id': int(headers['user-id']),'source': 'home'}
        response = s.post('https://wallet.3games.io/api/wallet/user_asset', headers=headers, json=json_data, timeout=10)
        
        if response.status_code != 200: return {'USDT': 0.0, 'WORLD': 0.0, 'BUILD': 0.0}
        data = response.json().get('data', {}).get('user_asset', {})
        return {
            'USDT': float(data.get('USDT', 0)),
            'WORLD': float(data.get('WORLD', 0)),
            'BUILD': float(data.get('BUILD', 0))
        }
    except Exception as e:
        prints(255, 0, 0, f'Lỗi khi lấy số dư: {e}')
        return {'USDT': 0.0, 'WORLD': 0.0, 'BUILD': 0.0}

def print_stats_cdtd(stats, s, headers, Coin):
    try:
        asset = user_asset(s, headers)
        prints(70, 240, 234, '📊 Thống kê phiên:')
        win_rate = stats["win"] / (stats["win"] + stats["lose"]) * 100 if (stats["win"] + stats["lose"]) > 0 else 0
        prints(50, 237, 65, f'🎯 Tỷ lệ thắng: {stats["win"]}/{stats["win"]+stats["lose"]} ({win_rate:.1f}%)')
        prints(50, 237, 65, f'🔥 Chuỗi thắng: {stats["streak"]} (Max: {stats["max_streak"]})')
        loi = asset.get(Coin, 0) - stats['asset_0']
        color = (0, 255, 20) if loi >= 0 else (255, 100, 100)
        symbol = "📈" if loi >= 0 else "📉"
        prints(*color, f"{symbol} Lợi nhuận: {loi:+.2f} {Coin}")
        
        best_logic = max(smart_ai.logic_performance.items(), key=lambda x: x[1]['win_rate'] if x[1]['total'] > 3 else -1)
        if best_logic[1]['total'] > 3:
            prints(150, 255, 150, f'🧠 Logic tốt nhất: #{best_logic[0]+1} ({best_logic[1]["win_rate"]:.1%})')
    except Exception as e:
        prints(255, 0, 0, f'❌ Lỗi thống kê: {e}')

def print_wallet(asset):
    prints(23, 232, 159, f'💰 USDT: {asset.get("USDT", 0):.2f} | 🌍 WORLD: {asset.get("WORLD", 0):.2f} | 🏗️ BUILD: {asset.get("BUILD", 0):.2f}'.center(60))

def bet_cdtd(s, headers, ki, kq, Coin, bet_amount):
    prints(255, 255, 0, f'💸 Đang đặt {bet_amount:.2f} {Coin} cho kì #{ki}...')
    try:
        json_data = {
            'issue_id': int(ki), 'bet_group': 'not_winner', 'asset_type': Coin,
            'athlete_id': int(kq), 'bet_amount': float(bet_amount),
        }
        response = s.post('https://api.sprintrun.win/sprint/bet', headers=headers, json=json_data, timeout=15)
        
        if response.status_code != 200:
            prints(255, 100, 0, f'⚠️ Lỗi HTTP: {response.status_code} - {response.text[:100]}')
            return
        
        response_json = response.json()
        if response_json.get('code') == 0 and response_json.get('msg') == 'ok':
            prints(0, 255, 19, f'✅ Đặt cược thành công: {bet_amount:.2f} {Coin} → Tránh {NV[int(kq)]}')
        else:
            prints(255, 100, 0, f'⚠️ Lỗi API: {response_json.get("msg", "Không rõ lỗi")}')
    except Exception as e:
        prints(255, 0, 0, f'❌ Lỗi khi đặt cược: {e}')

def main_cdtd():
    s = requests.Session()
    banner("CHẠY ĐUA TỐC ĐỘ")
    data = load_data_cdtd()
    headers = {
        'accept': '*/*', 'accept-language': 'vi,en;q=0.9', 'cache-control': 'no-cache',
        'country-code': 'vn', 'origin': 'https://xworld.info', 'pragma': 'no-cache',
        'priority': 'u=1, i', 'referer': 'https://xworld.info/', 'user-agent': 'Mozilla/5.0',
        'user-id': data['user-id'], 'user-login': 'login_v2',
        'user-secret-key': data['user-secret-key'], 'xb-language': 'vi-VN',
    }
    
    asset = user_asset(s, headers)
    print_wallet(asset)
    
    choice_txt = "    💰 Chọn loại tiền muốn chơi:\n        1️⃣ USDT\n        2️⃣ BUILD\n        3️⃣ WORLD"
    prints(219, 237, 138, choice_txt)
    coin_map = {'1': 'USDT', '2': 'BUILD', '3': 'WORLD'}
    while True:
        prints(125, 255, 168, 'Nhập loại tiền bạn muốn chơi (1/2/3):', end=' ')
        x = input()
        if x in coin_map:
            Coin = coin_map[x]
            break
        prints(247, 30, 30, 'Nhập sai, vui lòng nhập lại ...', end='\r')
        
    bet_amount0 = float(input(f'Nhập số {Coin} muốn đặt: '))
    heso = float(input('Nhập hệ số cược sau thua: '))
    delay1 = int(input('Sau bao nhiêu ván thì tạm nghỉ (Nhập 999 nếu không muốn): '))
    delay2 = int(input(f'Sau {delay1} ván thì tạm nghỉ bao nhiêu ván (Nhập 0 nếu không nghỉ): '))
    
    stats = {'win': 0, 'lose': 0, 'streak': 0, 'max_streak': 0, 'asset_0': asset.get(Coin, 0)}
    htr = []
    tong = 0

    while True:
        try:
            clear_screen()
            banner('CHẠY ĐUA TỐC ĐỘ')
            print_wallet(user_asset(s, headers))
            print_stats_cdtd(stats, s, headers, Coin)
            prints(247, 255, 97, "═" * 47)

            # Lấy dữ liệu top 10 và 100 mới nhất
            data_top10_cdtd = top_10_cdtd(s, headers)
            data_top100_cdtd = top_100_cdtd(s)
            
            # Xác định kì sẽ đặt cược là kì tiếp theo một cách đơn giản
            ki_dat_cuoc = data_top10_cdtd[0][0] + 1
            tong += 1

            # AI phân tích và chọn nhân vật
            kq, bet_amount = selected_NV(data_top10_cdtd, data_top100_cdtd, htr, heso, bet_amount0, data['user-id'], ki_dat_cuoc)
            
            # Logic tạm nghỉ
            cycle = delay1 + delay2
            pos = (tong - 1) % cycle if cycle > 0 else 0
            is_paused = pos >= delay1 and delay2 > 0

            if not is_paused:
                prints(0, 246, 255, f'🤖 AI chọn cược TRÁNH cho kì #{ki_dat_cuoc}: {NV[int(kq)]}')
                bet_cdtd(s, headers, ki_dat_cuoc, kq, Coin, bet_amount)
            else:
                prints(255, 255, 0, f'Ván này tạm nghỉ ({pos - delay1 + 1}/{delay2})')
                bet_amount = bet_amount0
                kq = None # Đặt kq là None để hàm kiem_tra_kq biết đây là ván nghỉ

            # Chờ đợi và kiểm tra kết quả của kì đã đặt cược
            result = kiem_tra_kq_cdtd(s, headers, kq, ki_dat_cuoc)

            # Cập nhật thống kê dựa trên kết quả
            if result is True:
                stats['win'] += 1
                stats['streak'] += 1
                stats['max_streak'] = max(stats['max_streak'], stats['streak'])
                htr.append({'kq': True, 'bet_amount': bet_amount})
            elif result is False:
                stats['streak'] = 0
                stats['lose'] += 1
                htr.append({'kq': False, 'bet_amount': bet_amount})
            elif result is None:
                prints(255, 255, 0, "⚠️ Không lấy được kết quả, bỏ qua ván cược.")

            prints(247, 255, 97, "--- Chuyển sang ván mới sau 20 giây ---")
            time.sleep(20)

        except Exception as e:
            prints(255, 0, 0, f'Lỗi trong vòng lặp chính: {e}. Thử lại sau 10 giây...')
            time.sleep(10)

if __name__ == "__main__":
    try:
        main_cdtd()
    except KeyboardInterrupt:
        prints(255, 100, 100, "\nChương trình đã dừng bởi người dùng.")
    except Exception as e:
        prints(255, 0, 0, f"\nĐã xảy ra lỗi nghiêm trọng: {e}")
