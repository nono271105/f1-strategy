import tkinter as tk
from tkinter import ttk, scrolledtext
import math
import numpy as np
from functools import lru_cache

class F1StrategyCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("F1 Strategy Calculator")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', foreground='black', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 11, 'bold'))
        style.configure('TFrame')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#e10600')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="F1 STRATEGY CALCULATOR", style='Title.TLabel')
        title.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Left panel - Inputs
        left_frame = ttk.LabelFrame(main_frame, text="Paramètres de course", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        row = 0
        
        # Basic race parameters
        ttk.Label(left_frame, text="Tours dans la course:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.laps_in_race = tk.StringVar(value="78")
        ttk.Entry(left_frame, textvariable=self.laps_in_race, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(left_frame, text="Tours complétés:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.laps_completed = tk.StringVar(value="0")
        ttk.Entry(left_frame, textvariable=self.laps_completed, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(left_frame, text="Temps pit stop (s):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.pit_stop_delta = tk.StringVar(value="22")
        ttk.Entry(left_frame, textvariable=self.pit_stop_delta, width=15).grid(row=row, column=1, pady=5)
        row += 1

        # Fuel parameters
        ttk.Label(left_frame, text="Carburant départ (kg):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.starting_fuel = tk.StringVar(value="110")
        ttk.Entry(left_frame, textvariable=self.starting_fuel, width=15).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(left_frame, text="Consommation / tour (kg):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.fuel_per_lap = tk.StringVar(value="1.5")
        ttk.Entry(left_frame, textvariable=self.fuel_per_lap, width=15).grid(row=row, column=1, pady=5)
        row += 1

        ttk.Label(left_frame, text="Temps / kg carburant (s/kg):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.fuel_time_per_kg = tk.StringVar(value="0.035")
        ttk.Entry(left_frame, textvariable=self.fuel_time_per_kg, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        # Starting compound
        ttk.Label(left_frame, text="Composé de départ:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.starting_compound = tk.StringVar(value="Any")
        compound_combo = ttk.Combobox(left_frame, textvariable=self.starting_compound, 
                                      values=["Any", "S", "M", "H"], width=13, state="readonly")
        compound_combo.grid(row=row, column=1, pady=5)
        row += 1
        
        ttk.Label(left_frame, text="Usure de départ (tours):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.starting_wear = tk.StringVar(value="0")
        ttk.Entry(left_frame, textvariable=self.starting_wear, width=15).grid(row=row, column=1, pady=5)
        row += 1
        
        # Must use two compounds
        self.must_use_two = tk.BooleanVar(value=True)
        ttk.Checkbutton(left_frame, text="2 composés obligatoires", 
                       variable=self.must_use_two).grid(row=row, column=0, columnspan=2, pady=10)
        row += 1
        
        # Separator
        ttk.Separator(left_frame, orient='horizontal').grid(row=row, column=0, columnspan=2, sticky='ew', pady=10)
        row += 1
        
        # SOFT tire parameters
        ttk.Label(left_frame, text="═══ SOFT ═══", foreground='#ff0000', 
                 font=('Arial', 11, 'bold')).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        ttk.Label(left_frame, text="Temps au tour neuf (s):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.soft_lap_time = tk.StringVar(value="71.112")
        ttk.Entry(left_frame, textvariable=self.soft_lap_time, width=15).grid(row=row, column=1, pady=2)
        row += 1
        
        ttk.Label(left_frame, text="Tours max:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.soft_max_laps = tk.StringVar(value="29")
        ttk.Entry(left_frame, textvariable=self.soft_max_laps, width=15).grid(row=row, column=1, pady=2)
        row += 1
        
        ttk.Label(left_frame, text="Dégradation/tour (s):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.soft_wear_rate = tk.StringVar(value="0.05")
        ttk.Entry(left_frame, textvariable=self.soft_wear_rate, width=15).grid(row=row, column=1, pady=2)
        row += 1
        
        # MEDIUM tire parameters
        ttk.Label(left_frame, text="═══ MEDIUM ═══", foreground='#ffff00', 
                 font=('Arial', 11, 'bold')).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        ttk.Label(left_frame, text="Temps au tour neuf (s):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.medium_lap_time = tk.StringVar(value="71.820")
        ttk.Entry(left_frame, textvariable=self.medium_lap_time, width=15).grid(row=row, column=1, pady=2)
        row += 1
        
        ttk.Label(left_frame, text="Tours max:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.medium_max_laps = tk.StringVar(value="39")
        ttk.Entry(left_frame, textvariable=self.medium_max_laps, width=15).grid(row=row, column=1, pady=2)
        row += 1
        
        ttk.Label(left_frame, text="Dégradation/tour (s):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.medium_wear_rate = tk.StringVar(value="0.04")
        ttk.Entry(left_frame, textvariable=self.medium_wear_rate, width=15).grid(row=row, column=1, pady=2)
        row += 1
        
        # HARD tire parameters
        ttk.Label(left_frame, text="═══ HARD ═══", foreground="#0A0909", 
                 font=('Arial', 11, 'bold')).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        ttk.Label(left_frame, text="Temps au tour neuf (s):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.hard_lap_time = tk.StringVar(value="72.500")
        ttk.Entry(left_frame, textvariable=self.hard_lap_time, width=15).grid(row=row, column=1, pady=2)
        row += 1
        
        ttk.Label(left_frame, text="Tours max:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.hard_max_laps = tk.StringVar(value="54")
        ttk.Entry(left_frame, textvariable=self.hard_max_laps, width=15).grid(row=row, column=1, pady=2)
        row += 1
        
        ttk.Label(left_frame, text="Dégradation/tour (s):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.hard_wear_rate = tk.StringVar(value="0.03")
        ttk.Entry(left_frame, textvariable=self.hard_wear_rate, width=15).grid(row=row, column=1, pady=2)
        row += 1
        
        # Calculate button
        calc_btn = tk.Button(left_frame, text="CALCULER LES STRATÉGIES", 
                            command=self.calculate_strategies,
                            bg='#e10600', fg='black', font=('Arial', 12, 'bold'),
                            cursor='hand2', relief=tk.RAISED, bd=3)
        calc_btn.grid(row=row, column=0, columnspan=2, pady=20, sticky='ew')
        
        # Right panel - Results
        right_frame = ttk.LabelFrame(main_frame, text="Résultats - Meilleures stratégies", padding="10")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(right_frame, width=70, height=40, 
                                                      font=('Courier', 10),
                                                      bg='#0a0a0a', fg='#00ff00',
                                                      insertbackground='white')
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
    def generate_wear_effect(self, max_laps, wear_rate):
        """Generate realistic 4-phase tire wear model:
        Phase 1 (Optimal): Laps 1-5, degradation ≈ 0 (warm-up phase)
        Phase 2 (Linear): Laps 6-80% of max_laps, degradation = wear_rate
        Phase 3 (Cliff): 80%-100% of max_laps, degradation ≈ 2x wear_rate (aging cliff)
        Phase 4 (Death): Beyond max_laps, very high penalty (returns None/invalid)
        """
        wear_effect = []
        br = float(wear_rate)
        ml = int(max_laps)
        cliff_threshold = int(0.8 * ml)
        
        for lap in range(ml + 1):
            if lap <= 5:
                # Phase 1: Optimal, minimal degradation during warm-up
                val = 0.0
            elif lap <= cliff_threshold:
                # Phase 2: Linear degradation
                val = (lap - 5) * br
            else:
                # Phase 3: Cliff degradation (accelerated aging)
                laps_in_cliff = lap - cliff_threshold
                linear_part = (cliff_threshold - 5) * br
                cliff_part = laps_in_cliff * br * 2.0  # 2x degradation in cliff
                val = linear_part + cliff_part
            
            wear_effect.append(val)
        return wear_effect

    def simulate_stint(self, laps, compound, starting_wear_idx, lap_times, wear_effects,
                       starting_fuel, fuel_per_lap, fuel_time_per_kg, first_stint=False):
        """Simulate a single stint with vectorized fuel consumption calculation.
        
        Returns (total_time, ending_wear_index, ending_fuel) or None if invalid.
        """
        wear = wear_effects[compound]
        base = lap_times[compound]
        
        # Check if stint is valid (doesn't exceed tire max laps)
        ending_wear_idx = starting_wear_idx + laps if first_stint else laps
        if ending_wear_idx >= len(wear):
            return None
        
        fuel_time_per_kg = float(fuel_time_per_kg)
        fuel_per = float(fuel_per_lap)
        
        # Calculate penalties: warm-up penalty on first lap
        penalty_first_lap = 0.8
        penalties = np.zeros(laps)
        if laps > 0:
            penalties[0] = penalty_first_lap
        
        # Get wear indices for each lap
        if first_stint:
            wear_indices = np.arange(starting_wear_idx, starting_wear_idx + laps)
        else:
            wear_indices = np.arange(laps)
        
        # Get wear penalties (vectorized)
        wear_penalties = np.array([wear[int(idx)] for idx in wear_indices])
        
        # Calculate fuel for each lap (decreasing due to consumption)
        fuel_levels = starting_fuel - np.arange(laps) * fuel_per
        fuel_penalties = fuel_levels * fuel_time_per_kg
        
        # Total lap times: base + wear + fuel penalty + first-lap penalty
        lap_times_array = base + wear_penalties + fuel_penalties + penalties
        
        total_time = np.sum(lap_times_array)
        ending_fuel = max(0.0, starting_fuel - laps * fuel_per)
        
        return total_time, int(ending_wear_idx), ending_fuel
    
    def zero_stop(self, laps_left, lap_times, wear_effects, starting_wear, compound):
        # Simulate single continuous stint using fuel and wear model
        starting_fuel = float(self.starting_fuel.get())
        fuel_per_lap = float(self.fuel_per_lap.get())
        time_per_kg = float(self.fuel_time_per_kg.get())

        res = self.simulate_stint(laps_left, compound, starting_wear, lap_times, wear_effects,
                                  starting_fuel, fuel_per_lap, time_per_kg, first_stint=True)
        if not res:
            return None
        total_time, _, _ = res

        return {
            'compounds': [compound, '', '', ''],
            'stint_lengths': [laps_left, 0, 0, 0],
            'total_time': total_time
        }
    
    def one_stop(self, laps_left, lap_times, wear_effects, starting_wear, c1, c2, pit_delta):
        # Try all possible split points for a single pitstop: first stint L1, second L2
        starting_fuel = float(self.starting_fuel.get())
        fuel_per_lap = float(self.fuel_per_lap.get())
        time_per_kg = float(self.fuel_time_per_kg.get())

        best = None
        # Optimisation: increment by 2 pour réduire les itérations (granularité réduite)
        for l1 in range(1, laps_left, max(1, laps_left // 30)):
            l2 = laps_left - l1

            s1 = self.simulate_stint(l1, c1, starting_wear, lap_times, wear_effects,
                                     starting_fuel, fuel_per_lap, time_per_kg, first_stint=True)
            if not s1:
                continue
            t1, _, fuel_after_s1 = s1

            s2 = self.simulate_stint(l2, c2, 0, lap_times, wear_effects,
                                     fuel_after_s1, fuel_per_lap, time_per_kg, first_stint=False)
            if not s2:
                continue
            t2, _, _ = s2

            total_time = t1 + pit_delta + t2

            candidate = {
                'compounds': [c1, c2, '', ''],
                'stint_lengths': [l1, l2, 0, 0],
                'total_time': total_time
            }
            if best is None or candidate['total_time'] < best['total_time']:
                best = candidate

        return best
    
    def two_stop(self, laps_left, lap_times, wear_effects, starting_wear, c1, c2, c3, pit_delta):
        # Try all combinations of two pitstops (split into l1, l2, l3)
        # Optimisation: réduire granularité avec un pas adapté au nombre de tours
        starting_fuel = float(self.starting_fuel.get())
        fuel_per_lap = float(self.fuel_per_lap.get())
        time_per_kg = float(self.fuel_time_per_kg.get())

        best = None
        step = max(1, laps_left // 20)  # Réduire le nombre d'itérations significativement
        
        for l1 in range(1, laps_left - 1, step):
            for l2 in range(1, laps_left - l1, step):
                l3 = laps_left - l1 - l2

                s1 = self.simulate_stint(l1, c1, starting_wear, lap_times, wear_effects,
                                         starting_fuel, fuel_per_lap, time_per_kg, first_stint=True)
                if not s1:
                    continue
                t1, _, fuel_after_s1 = s1

                s2 = self.simulate_stint(l2, c2, 0, lap_times, wear_effects,
                                         fuel_after_s1, fuel_per_lap, time_per_kg, first_stint=False)
                if not s2:
                    continue
                t2, _, fuel_after_s2 = s2

                s3 = self.simulate_stint(l3, c3, 0, lap_times, wear_effects,
                                         fuel_after_s2, fuel_per_lap, time_per_kg, first_stint=False)
                if not s3:
                    continue
                t3, _, _ = s3

                total_time = t1 + pit_delta + t2 + pit_delta + t3

                candidate = {
                    'compounds': [c1, c2, c3, ''],
                    'stint_lengths': [l1, l2, l3, 0],
                    'total_time': total_time
                }
                if best is None or candidate['total_time'] < best['total_time']:
                    best = candidate

        return best
    
    def calculate_undercut_score(self, strategy, pit_delta, wear_effects, lap_times):
        """Calculate Undercut/Overcut score between -10 and +10.
        
        Negative scores (-10 to -5): Undercut favorable (tires degrade quickly = pit early)
        Positive scores (+5 to +10): Overcut favorable (durable tires = stay out longer)
        Neutral scores (±2): Balanced
        
        Args:
            strategy: dict with 'compounds' and 'stint_lengths'
            pit_delta: pit stop time in seconds
            wear_effects: dict mapping compound -> list of wear penalties
            lap_times: dict mapping compound -> lap time
        
        Returns:
            float: score between -10 and +10
        """
        score = 0.0
        compounds_used = [c for c in strategy['compounds'] if c != '']
        stint_lengths = [s for s in strategy['stint_lengths'] if s != 0]
        
        if not compounds_used:
            return score
        
        # Criterion 1: Average tire degradation over the stint
        # Calculate average wear rate for each compound used
        avg_degradations = []
        for compound in compounds_used:
            wear = wear_effects[compound]
            if len(wear) > 6:  # Only consider after warm-up phase
                # Get linear wear phase (laps 6 to 80% of max)
                wear_values = wear[6:int(len(wear) * 0.8)]
                if wear_values:
                    laps_in_phase = len(wear_values)
                    avg_deg = (wear_values[-1] - wear_values[0]) / max(1, laps_in_phase - 1)
                    avg_degradations.append(avg_deg)
            else:
                avg_degradations.append(0.0)
        
        if avg_degradations:
            avg_deg_overall = sum(avg_degradations) / len(avg_degradations)
            
            # High degradation (fast, fragile tires) → Undercut favorable
            if avg_deg_overall > 0.04:
                score -= 8  # Strong undercut signal
            # Low degradation (durable tires) → Overcut favorable
            elif avg_deg_overall < 0.035:
                score += 8  # Strong overcut signal
            # Else: neutral (score stays near 0)
        
        # Criterion 2: Pit stop duration
        # Long pit stops make undercut more favorable (pit early to minimize loss)
        if pit_delta > 23.0:
            score -= 1  # Slightly favor undercut
        elif pit_delta < 22.0:
            score += 1  # Slightly favor overcut
        
        # Criterion 3: Stint distribution
        if len(stint_lengths) >= 2:
            stint_1 = stint_lengths[0]
            avg_other = sum(stint_lengths[1:]) / len(stint_lengths[1:])
            
            # Undercut: first stint much shorter than others (pit early, new tires early)
            if stint_1 < avg_other * 0.7:  # First stint significantly shorter
                score -= 2
            # Overcut: first stint much longer than others (stay out, late pit)
            elif stint_1 > avg_other * 1.3:  # First stint significantly longer
                score += 2
        
        # Clamp score between -10 and +10
        score = max(-10.0, min(10.0, score))
        
        return score
    
    def get_compound_name(self, compound):
        names = {'S': 'Soft', 'M': 'Medium', 'H': 'Hard'}
        return names.get(compound, '')
    
    def format_time(self, total_seconds):
        """Format time in seconds to h:min:sec:ms format"""
        hours = int(total_seconds // 3600)
        remaining = total_seconds % 3600
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        milliseconds = int((total_seconds % 1) * 1000)
        
        return f"{hours}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
    
    def calculate_strategies(self):
        """Main calculation function"""
        try:
            # Clear previous results
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "⏳ Calcul en cours...\n\n")
            self.root.update()
            
            # Get inputs
            laps_in_race = int(self.laps_in_race.get())
            laps_completed = int(self.laps_completed.get())
            laps_left = laps_in_race - laps_completed
            
            pit_delta = float(self.pit_stop_delta.get())
            starting_compound = self.starting_compound.get()
            starting_wear = int(self.starting_wear.get())
            must_use_two = self.must_use_two.get()
            
            # Lap times
            lap_times = {
                'S': float(self.soft_lap_time.get()),
                'M': float(self.medium_lap_time.get()),
                'H': float(self.hard_lap_time.get())
            }
            
            # Generate wear effects
            wear_effects = {
                'S': self.generate_wear_effect(int(self.soft_max_laps.get()), 
                                               float(self.soft_wear_rate.get())),
                'M': self.generate_wear_effect(int(self.medium_max_laps.get()), 
                                               float(self.medium_wear_rate.get())),
                'H': self.generate_wear_effect(int(self.hard_max_laps.get()), 
                                               float(self.hard_wear_rate.get()))
            }
            
            strategies = []
            compounds = ['S', 'M', 'H'] if starting_compound == 'Any' else [starting_compound]
            all_compounds = ['S', 'M', 'H']
            
            # Zero-stop
            if not must_use_two:
                for c1 in compounds:
                    result = self.zero_stop(laps_left, lap_times, wear_effects, starting_wear, c1)
                    if result:
                        strategies.append(result)
            
            # One-stop
            for c1 in compounds:
                for c2 in all_compounds:
                    if must_use_two and c1 == c2:
                        continue
                    result = self.one_stop(laps_left, lap_times, wear_effects, starting_wear, c1, c2, pit_delta)
                    if result:
                        strategies.append(result)
            
            # Two-stop
            for c1 in compounds:
                for c2 in all_compounds:
                    for c3 in all_compounds:
                        if must_use_two and c1 == c2 == c3:
                            continue
                        result = self.two_stop(laps_left, lap_times, wear_effects, starting_wear, c1, c2, c3, pit_delta)
                        if result:
                            strategies.append(result)
            
            # Calculate undercut/overcut score for each strategy
            for strategy in strategies:
                strategy['undercut_score'] = self.calculate_undercut_score(
                    strategy, pit_delta, wear_effects, lap_times
                )
            
            # Sort by total time, then by undercut score (negative first = undercut favorable)
            # Negative scores (undercut) appear first, then positive scores (overcut)
            strategies.sort(key=lambda x: (x['total_time'], x.get('undercut_score', 0)))
            
            # Display results
            self.results_text.delete(1.0, tk.END)
            
            # Title centered
            title = "TOP 10 MEILLEURES STRATÉGIES"
            self.results_text.insert(tk.END, f"\n{title:^60}\n")
            self.results_text.insert(tk.END, "═" * 60 + "\n\n")
            
            for idx, strategy in enumerate(strategies[:10]):
                self.results_text.insert(tk.END, f"{'─' * 60}\n")
                if idx == 0:
                    self.results_text.insert(tk.END, f"  STRATÉGIE OPTIMALE #{idx + 1}\n")
                else:
                    self.results_text.insert(tk.END, f"  #{idx + 1}\n")
                self.results_text.insert(tk.END, f"{'─' * 60}\n")
                
                formatted_time = self.format_time(strategy['total_time'])
                self.results_text.insert(tk.END, f"  Temps total: {formatted_time}\n")
                
                # Display undercut/overcut strategy type
                undercut_score = strategy.get('undercut_score', 0)
                if undercut_score < -3:
                    strategy_type = "[UNDERCUT]"
                elif undercut_score > 3:
                    strategy_type = "[OVERCUT]"
                else:
                    strategy_type = "[NEUTRE]"
                self.results_text.insert(tk.END, f"  {strategy_type}\n\n")
                
                num_stops = sum(1 for c in strategy['compounds'] if c != '') - 1
                self.results_text.insert(tk.END, f"  Nombre d'arrêts: {num_stops}\n\n")
                
                for stint_idx, compound in enumerate(strategy['compounds']):
                    if compound == '':
                        break
                    
                    stint_length = strategy['stint_lengths'][stint_idx]
                    compound_name = self.get_compound_name(compound)
                    
                    if compound == 'S':
                        icon = '🔴'
                    elif compound == 'M':
                        icon = '🟡'
                    else:
                        icon = '⚪'
                    
                    self.results_text.insert(tk.END, f"  {icon} Stint {stint_idx + 1}: {compound_name:7} → {stint_length:2} tours\n")
                
                self.results_text.insert(tk.END, "\n")
            
            self.results_text.insert(tk.END, "═" * 60 + "\n")
            self.results_text.insert(tk.END, f"✓ {len(strategies)} stratégies calculées au total\n")
            
        except Exception as e:
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"❌ ERREUR: {str(e)}\n")
            self.results_text.insert(tk.END, "\nVérifiez que tous les champs sont correctement remplis.")

if __name__ == "__main__":
    root = tk.Tk()
    app = F1StrategyCalculator(root)
    root.mainloop()
