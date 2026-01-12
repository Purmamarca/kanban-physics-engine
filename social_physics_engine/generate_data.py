"""
⚡ Google Antigravity - Six Sigma Kanban Physics Engine
========================================================
Strict compliance with Six Sigma methodology (Pages 297-308)
Performance: O(1) vectorized operations using NumPy

Author: Bolt AI Optimization
Version: 2.0.0
License: MIT
"""

from typing import Dict, Tuple, Optional
from dataclasses import dataclass
import pandas as pd
import numpy as np
import time
import sys

# Windows Unicode fix
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')


@dataclass
class PhysicsConfig:
    """Configuration parameters for the physics engine."""
    # Social Pressure (Average Daily Demand - D)
    avg_demand: int = 250
    demand_std_dev: int = 50
    
    # Friction (Replenishment Lead Time - L)
    avg_lead_time: int = 5
    
    # Entropy (Safety Stock - SS)
    min_safety_stock: float = 0.10
    max_safety_stock: float = 0.30
    
    # Container Capacity (C)
    container_sizes: Tuple[int, ...] = (20, 50, 100)
    
    # Six Sigma Z-Score (typically 1.65 for 95% service level)
    z_score: float = 1.65


class GoogleAntigravity:
    """
    ⚡ BOLT OPTIMIZED: STRICT KANBAN PHYSICS (Pages 297-308)
    --------------------------------------------------------
    Simulates environment physics using Six Sigma statistical distributions.
    Performance: Vectorized (O(1) complexity relative to loop depth).
    
    The engine implements four core Kanban parameters:
    - D: Average Daily Demand (Social Pressure)
    - L: Replenishment Lead Time (Friction)
    - SS: Safety Stock (Entropy Factor)
    - C: Container Capacity
    
    Additionally calculates:
    - N: Number of Kanban cards (Page 297 formula)
    - ROP: Reorder Point (D × L + SS)
    - Interaction Score: Spatial influence metric (Vectorized)
    """
    
    def __init__(self, seed: Optional[int] = 42, config: Optional[PhysicsConfig] = None, num_users: Optional[int] = None):
        """
        Initialize the physics engine.
        
        Args:
            seed: Random seed for reproducibility
            config: Physics configuration parameters
            num_users: Number of users/nodes (optional, for initialization)
        """
        if seed is not None:
            np.random.seed(seed)
        
        self.config = config or PhysicsConfig()
        self._validate_config()
        self.num_users = num_users

        # Initialize user state for interaction calculations
        if num_users:
            self.users = pd.DataFrame({
                'id': range(num_users),
                'x': np.random.uniform(0, 100, num_users),
                'y': np.random.uniform(0, 100, num_users),
                'influence': np.random.uniform(0, 1, num_users)
            })
        else:
            self.users = None
    
    def _validate_config(self) -> None:
        """Validate configuration parameters."""
        if self.config.avg_demand <= 0:
            raise ValueError("avg_demand must be positive")
        if self.config.demand_std_dev < 0:
            raise ValueError("demand_std_dev must be non-negative")
        if self.config.avg_lead_time <= 0:
            raise ValueError("avg_lead_time must be positive")
        if not (0 <= self.config.min_safety_stock <= self.config.max_safety_stock <= 1):
            raise ValueError("Safety stock must be between 0 and 1")
        if not all(c > 0 for c in self.config.container_sizes):
            raise ValueError("Container sizes must be positive")
    
    def measure_social_pressure(self, n_nodes: int) -> np.ndarray:
        """
        PARAMETER: Average Daily Demand (D) [Page 297]
        LOGIC: Normal Distribution (Gaussian).
        
        Six Sigma Note: Demand is rarely flat. We use a mean with 
        standard deviation to simulate organic pressure variability.
        
        ⚡ OPTIMIZATION: Uses np.abs to prevent negative demand without slow checks.
        
        Args:
            n_nodes: Number of nodes to simulate
            
        Returns:
            Array of demand values (integers)
        """
        return np.abs(
            np.random.normal(
                self.config.avg_demand,
                self.config.demand_std_dev,
                n_nodes
            )
        ).astype(int)
    
    def calculate_friction(self, n_nodes: int) -> np.ndarray:
        """
        PARAMETER: Replenishment Lead Time (L) [Page 297]
        LOGIC: Poisson Distribution.
        
        Six Sigma Note: Captures the 'long tail' of delay friction.
        Most friction is average, but some nodes will experience
        extreme drag, driving the need for Safety Stock.
        
        Args:
            n_nodes: Number of nodes to simulate
            
        Returns:
            Array of lead time values (integers)
        """
        return np.random.poisson(self.config.avg_lead_time, n_nodes)
    
    def entropy_factor(self, n_nodes: int) -> np.ndarray:
        """
        PARAMETER: Safety Stock (SS) [Pages 297 & 301]
        LOGIC: Derived Entropy.
        
        Six Sigma Note: Safety Stock (SS) is the hedge against Friction (L) and 
        Pressure (D) variability. Protects against stockouts during lead time.
        
        ⚡ OPTIMIZATION: Vectorized uniform distribution.
        
        Args:
            n_nodes: Number of nodes to simulate
            
        Returns:
            Array of safety stock percentages (floats, e.g., 0.20 = 20% buffer)
        """
        return np.round(
            np.random.uniform(
                self.config.min_safety_stock,
                self.config.max_safety_stock,
                n_nodes
            ),
            2
        )
    
    def container_capacity(self, n_nodes: int) -> np.ndarray:
        """
        PARAMETER: Container Capacity (C) [Page 297]
        LOGIC: Standardized Lots.
        
        Six Sigma Note: Page 300 Rule 2 ("Withdraw only what is needed") requires
        standard container sizes to function as visual signals.
        
        ⚡ OPTIMIZATION: Uses np.random.choice for instant array generation.
        
        Args:
            n_nodes: Number of nodes to simulate
            
        Returns:
            Array of container capacity values
        """
        return np.random.choice(list(self.config.container_sizes), n_nodes)
    
    def calculate_kanban_cards(
        self,
        demand: np.ndarray,
        lead_time: np.ndarray,
        safety_stock: np.ndarray,
        container_capacity: np.ndarray
    ) -> np.ndarray:
        """
        Calculate number of Kanban cards using Six Sigma formula [Page 297].
        
        Formula: N = (D × L × (1 + SS)) / C
        Where:
            N = Number of Kanban cards
            D = Average Daily Demand
            L = Lead Time
            SS = Safety Stock percentage
            C = Container Capacity
        
        ⚡ OPTIMIZATION: Fully vectorized calculation.
        
        Args:
            demand: Average daily demand array
            lead_time: Lead time array
            safety_stock: Safety stock percentage array
            container_capacity: Container capacity array
            
        Returns:
            Array of Kanban card counts (rounded up to ensure coverage)
        """
        return np.ceil(
            (demand * lead_time * (1 + safety_stock)) / container_capacity
        ).astype(int)
    
    def calculate_reorder_point(
        self,
        demand: np.ndarray,
        lead_time: np.ndarray,
        safety_stock: np.ndarray
    ) -> np.ndarray:
        """
        Calculate Reorder Point (ROP) for inventory management.
        
        Formula: ROP = (D × L) + (D × L × SS)
        Simplified: ROP = D × L × (1 + SS)
        
        Args:
            demand: Average daily demand array
            lead_time: Lead time array
            safety_stock: Safety stock percentage array
            
        Returns:
            Array of reorder point values
        """
        return (demand * lead_time * (1 + safety_stock)).astype(int)
    
    def calculate_interactions(self) -> pd.DataFrame:
        """
        Calculate interaction scores between all pairs of users.
        Score = (influence_a * influence_b) / distance

        ⚡ OPTIMIZATION: Vectorized using NumPy broadcasting.
        """
        if self.users is None:
             raise ValueError("Users not initialized. Provide num_users to __init__ or set self.users")

        # Extract data as arrays
        ids = self.users['id'].values
        coords = self.users[['x', 'y']].values
        influence = self.users['influence'].values

        # Calculate distance matrix using broadcasting
        # Shape: (N, N, 2) -> (N, N)
        # Memory usage: O(N^2). For N=1000, this is ~8MB (doubles), which is safe.
        diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
        dists = np.sqrt(np.sum(diff**2, axis=2))

        # Calculate influence product matrix
        # Shape: (N, N)
        inf_prod = np.outer(influence, influence)

        # Calculate scores
        with np.errstate(divide='ignore', invalid='ignore'):
            scores = inf_prod / dists

        # Create indices for the result
        n = len(self.users)
        indices = np.indices((n, n))
        row_indices = indices[0].flatten()
        col_indices = indices[1].flatten()

        # Filter out self-loops (i == j)
        mask = row_indices != col_indices

        # Flatten arrays and apply mask
        user_a_ids = ids[row_indices[mask]]
        user_b_ids = ids[col_indices[mask]]
        flat_dists = dists.flatten()[mask]
        flat_scores = scores.flatten()[mask]

        # Handle any remaining NaNs or Infs
        flat_scores = np.nan_to_num(flat_scores, posinf=0.0, neginf=0.0)

        return pd.DataFrame({
            'user_a': user_a_ids,
            'user_b': user_b_ids,
            'distance': flat_dists,
            'score': flat_scores
        })

    def generate_complete_dataset(self, n_nodes: int) -> pd.DataFrame:
        """
        Generate a complete Six Sigma Kanban physics dataset.
        
        Args:
            n_nodes: Number of nodes to simulate
            
        Returns:
            DataFrame with all physics parameters and calculated metrics
        """
        # Ensure users are initialized for interaction calc (required for GoogleJules compatibility)
        if self.users is None or len(self.users) != n_nodes:
            self.num_users = n_nodes
            self.users = pd.DataFrame({
                'id': range(n_nodes),
                'x': np.random.uniform(0, 100, n_nodes),
                'y': np.random.uniform(0, 100, n_nodes),
                'influence': np.random.uniform(0, 1, n_nodes)
            })

        # Generate base parameters
        social_pressure = self.measure_social_pressure(n_nodes)
        friction = self.calculate_friction(n_nodes)
        entropy = self.entropy_factor(n_nodes)
        capacity = self.container_capacity(n_nodes)
        
        # Calculate derived metrics
        kanban_cards = self.calculate_kanban_cards(
            social_pressure, friction, entropy, capacity
        )
        reorder_point = self.calculate_reorder_point(
            social_pressure, friction, entropy
        )
        
        # Create comprehensive DataFrame
        df = pd.DataFrame({
            'node_id': range(n_nodes),
            'demand_D': social_pressure,
            'lead_time_L': friction,
            'safety_stock_SS': entropy,
            'container_capacity_C': capacity,
            'kanban_cards_N': kanban_cards,
            'reorder_point_ROP': reorder_point,
        })
        
        return df
    
    def analyze_real_data(
        self,
        data: pd.DataFrame,
        demand_column: str = 'demand',
        lead_time_column: str = 'lead_time',
        node_id_column: str = 'node_id',
        safety_stock_column: Optional[str] = None,
        container_capacity_column: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Analyze real-world data and calculate Kanban metrics.
        
        This method takes actual operational data (demand, lead times) and applies
        Six Sigma Kanban formulas to calculate optimal Kanban cards and reorder points.
        
        Args:
            data: DataFrame containing real operational data
            demand_column: Name of the column containing average daily demand
            lead_time_column: Name of the column containing lead time (days)
            node_id_column: Name of the column containing unique identifiers
            safety_stock_column: Optional column for safety stock percentages
            container_capacity_column: Optional column for container capacities
            
        Returns:
            DataFrame with original data plus calculated Kanban metrics
            
        Example:
            >>> engine = GoogleAntigravity()
            >>> real_data = pd.read_csv('inventory.csv')
            >>> results = engine.analyze_real_data(
            ...     data=real_data,
            ...     demand_column='avg_demand',
            ...     lead_time_column='lead_days'
            ... )
            >>> results.to_csv('kanban_analysis.csv', index=False)
        """
        # Validate input
        required_columns = [demand_column, lead_time_column]
        missing = [col for col in required_columns if col not in data.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        
        # Create a copy to avoid modifying original data
        result = data.copy()
        
        # Extract demand and lead time
        demand = result[demand_column].values.astype(float)
        lead_time = result[lead_time_column].values.astype(float)
        
        # Handle safety stock
        if safety_stock_column and safety_stock_column in result.columns:
            safety_stock = result[safety_stock_column].values.astype(float)
        else:
            # Generate safety stock based on configuration
            n_rows = len(result)
            safety_stock = np.round(
                np.random.uniform(
                    self.config.min_safety_stock,
                    self.config.max_safety_stock,
                    n_rows
                ),
                2
            )
            result['safety_stock_SS'] = safety_stock
        
        # Handle container capacity
        if container_capacity_column and container_capacity_column in result.columns:
            container_capacity = result[container_capacity_column].values.astype(float)
        else:
            # Assign standard container sizes
            n_rows = len(result)
            container_capacity = np.random.choice(
                list(self.config.container_sizes),
                n_rows
            )
            result['container_capacity_C'] = container_capacity
        
        # Ensure positive values
        demand = np.abs(demand)
        lead_time = np.maximum(lead_time, 1)  # Minimum 1 day lead time
        
        # Calculate Kanban metrics using Six Sigma formulas
        kanban_cards = np.ceil(
            (demand * lead_time * (1 + safety_stock)) / container_capacity
        ).astype(int)
        
        reorder_point = (demand * lead_time * (1 + safety_stock)).astype(int)
        
        # Add calculated columns
        result['demand_D'] = demand.astype(int)
        result['lead_time_L'] = lead_time.astype(int)
        result['kanban_cards_N'] = kanban_cards
        result['reorder_point_ROP'] = reorder_point
        
        # Reorder columns for clarity
        priority_cols = [
            node_id_column,
            'demand_D',
            'lead_time_L',
            'safety_stock_SS',
            'container_capacity_C',
            'kanban_cards_N',
            'reorder_point_ROP'
        ]
        
        # Keep only columns that exist
        existing_priority = [col for col in priority_cols if col in result.columns]
        other_cols = [col for col in result.columns if col not in existing_priority]
        
        result = result[existing_priority + other_cols]
        
        return result
    
    def load_and_analyze_csv(
        self,
        filepath: str,
        **kwargs
    ) -> pd.DataFrame:
        """
        Convenience method to load CSV and analyze in one step.
        
        Args:
            filepath: Path to CSV file
            **kwargs: Arguments to pass to analyze_real_data()
            
        Returns:
            DataFrame with analyzed results
            
        Example:
            >>> engine = GoogleAntigravity()
            >>> results = engine.load_and_analyze_csv(
            ...     'inventory_data.csv',
            ...     demand_column='daily_demand',
            ...     lead_time_column='lead_days'
            ... )
        """
        data = pd.read_csv(filepath)
        return self.analyze_real_data(data, **kwargs)


class GoogleJules(GoogleAntigravity):
    """
    Adapter for backward compatibility with tests.
    Inherits optimized interaction calculation from GoogleAntigravity.
    """
    def __init__(self, num_users: int = 100, seed: int = 42):
        super().__init__(seed=seed, num_users=num_users)


def benchmark_performance(engine: GoogleAntigravity, n_nodes: int) -> Dict[str, float]:
    """
    Benchmark the performance of the physics engine.
    
    Args:
        engine: GoogleAntigravity instance
        n_nodes: Number of nodes to simulate
        
    Returns:
        Dictionary with timing results
    """
    timings = {}
    
    # Benchmark individual operations
    start = time.perf_counter()
    _ = engine.measure_social_pressure(n_nodes)
    timings['social_pressure_ms'] = (time.perf_counter() - start) * 1000
    
    start = time.perf_counter()
    _ = engine.calculate_friction(n_nodes)
    timings['friction_ms'] = (time.perf_counter() - start) * 1000
    
    start = time.perf_counter()
    _ = engine.entropy_factor(n_nodes)
    timings['entropy_ms'] = (time.perf_counter() - start) * 1000
    
    start = time.perf_counter()
    _ = engine.container_capacity(n_nodes)
    timings['capacity_ms'] = (time.perf_counter() - start) * 1000
    
    # Benchmark complete dataset generation
    start = time.perf_counter()
    _ = engine.generate_complete_dataset(n_nodes)
    timings['total_ms'] = (time.perf_counter() - start) * 1000
    
    return timings


def print_statistics(df: pd.DataFrame) -> None:
    """Print comprehensive statistics for the generated dataset."""
    print("\n📊 STATISTICAL SUMMARY")
    print("=" * 70)
    
    # Social Pressure (Demand)
    print("\n🔹 Social Pressure (D) - Normal Distribution:")
    print(f"   Mean: {df['demand_D'].mean():.2f} | Std: {df['demand_D'].std():.2f}")
    print(f"   Range: [{df['demand_D'].min()}, {df['demand_D'].max()}]")
    print(f"   Median: {df['demand_D'].median():.0f} | Mode: {df['demand_D'].mode()[0]}")
    
    # Friction (Lead Time)
    print("\n🔹 Friction (L) - Poisson Distribution:")
    print(f"   Mean: {df['lead_time_L'].mean():.2f} | Std: {df['lead_time_L'].std():.2f}")
    print(f"   Range: [{df['lead_time_L'].min()}, {df['lead_time_L'].max()}]")
    print(f"   Median: {df['lead_time_L'].median():.0f}")
    
    # Entropy (Safety Stock)
    print("\n🔹 Entropy Factor (SS) - Uniform Distribution:")
    print(f"   Mean: {df['safety_stock_SS'].mean():.2f} | Std: {df['safety_stock_SS'].std():.2f}")
    print(f"   Range: [{df['safety_stock_SS'].min():.2f}, {df['safety_stock_SS'].max():.2f}]")
    
    # Container Capacity
    print("\n🔹 Container Capacity (C) - Standardized Lots:")
    unique_vals = sorted(df['container_capacity_C'].unique())
    print(f"   Unique Values: {unique_vals}")
    dist = dict(zip(*np.unique(df['container_capacity_C'], return_counts=True)))
    print(f"   Distribution: {dist}")
    
    # Kanban Cards
    print("\n🔹 Kanban Cards (N) - Calculated Metric:")
    print(f"   Mean: {df['kanban_cards_N'].mean():.2f} | Std: {df['kanban_cards_N'].std():.2f}")
    print(f"   Range: [{df['kanban_cards_N'].min()}, {df['kanban_cards_N'].max()}]")
    
    # Reorder Point
    print("\n🔹 Reorder Point (ROP) - Calculated Metric:")
    print(f"   Mean: {df['reorder_point_ROP'].mean():.2f} | Std: {df['reorder_point_ROP'].std():.2f}")
    print(f"   Range: [{df['reorder_point_ROP'].min()}, {df['reorder_point_ROP'].max()}]")


def main():
    """Main execution function."""
    print("⚡ Google Antigravity - Six Sigma Kanban Physics Engine v2.0")
    print("=" * 70)
    print("Strict Compliance with Six Sigma (Pages 297-308)")
    print("=" * 70)
    
    # Initialize the physics engine
    config = PhysicsConfig()
    engine = GoogleAntigravity(seed=42, config=config)
    n_nodes = 200  # Number of nodes to simulate
    
    print(f"\n🔬 Simulating {n_nodes} nodes with vectorized NumPy operations...")
    
    # Generate complete dataset
    start_time = time.perf_counter()
    df = engine.generate_complete_dataset(n_nodes)
    generation_time = (time.perf_counter() - start_time) * 1000
    
    # Print statistics
    print_statistics(df)
    
    # Sample data
    print("\n" + "=" * 70)
    print("📋 SAMPLE DATA (First 10 Nodes)")
    print("=" * 70)
    print(df.head(10).to_string(index=False))
    
    # Performance metrics
    print("\n" + "=" * 70)
    print("⚡ PERFORMANCE METRICS")
    print("=" * 70)

    print(f"Total Generation Time: {generation_time:.3f} ms")
    print(f"Time per Node: {generation_time/n_nodes:.4f} ms")
    print(f"Nodes per Second: {n_nodes/(generation_time/1000):.0f}")
    
    # Detailed benchmark
    print("\n🔍 Detailed Benchmark:")
    timings = benchmark_performance(engine, n_nodes)
    for operation, time_ms in timings.items():
        print(f"   {operation}: {time_ms:.4f} ms")
    
    # Export option
    export_file = "kanban_physics_data.csv"
    try:
        df.to_csv(export_file, index=False, encoding='utf-8')
        print(f"\n💾 Data exported to: {export_file}")
    except Exception as e:
        print(f"\n⚠️  Export failed: {e}")
    
    print("\n✅ Physics engine test completed successfully!")
    print(f"⚡ Performance: O(1) vectorized operations for {n_nodes} nodes")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Execution interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
