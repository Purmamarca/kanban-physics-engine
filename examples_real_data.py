"""
Example: Analyzing Real Inventory Data with Kanban Physics Engine
==================================================================

This script demonstrates how to use the Kanban Physics Engine with
real-world inventory data.
"""

from social_physics_engine.generate_data import GoogleAntigravity, PhysicsConfig
import pandas as pd
import os


def example_1_basic_analysis():
    """Example 1: Basic analysis of real inventory data."""
    print("=" * 70)
    print("EXAMPLE 1: Basic Real Data Analysis")
    print("=" * 70)
    
    # Initialize engine
    engine = GoogleAntigravity(seed=42)
    
    # Load example data
    data_path = os.path.join('data', 'example_inventory.csv')
    
    if os.path.exists(data_path):
        # Analyze the data
        results = engine.load_and_analyze_csv(
            data_path,
            demand_column='demand',
            lead_time_column='lead_time',
            node_id_column='node_id'
        )
        
        print("\n📊 Analysis Results:")
        print(results[['node_id', 'product_name', 'demand_D', 'lead_time_L', 
                       'kanban_cards_N', 'reorder_point_ROP']])
        
        # Save results
        output_path = 'inventory_analysis_results.csv'
        results.to_csv(output_path, index=False)
        print(f"\n✅ Results saved to: {output_path}")
    else:
        print(f"⚠️  Example data file not found: {data_path}")
        print("Creating sample data for demonstration...")
        
        # Create sample data
        sample_data = pd.DataFrame({
            'node_id': [f'SKU-{i:03d}' for i in range(1, 11)],
            'demand': [250, 180, 420, 95, 310, 275, 150, 380, 210, 165],
            'lead_time': [5, 3, 7, 2, 6, 4, 5, 8, 3, 4],
            'product_name': [f'Product {chr(65+i)}' for i in range(10)]
        })
        
        # Analyze
        results = engine.analyze_real_data(
            sample_data,
            demand_column='demand',
            lead_time_column='lead_time',
            node_id_column='node_id'
        )
        
        print("\n📊 Analysis Results:")
        print(results[['node_id', 'product_name', 'demand_D', 'lead_time_L', 
                       'kanban_cards_N', 'reorder_point_ROP']])


def example_2_custom_configuration():
    """Example 2: Analysis with custom Six Sigma parameters."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Custom Configuration for High-Variability Environment")
    print("=" * 70)
    
    # Custom config for high-variability supply chain
    config = PhysicsConfig(
        avg_demand=300,
        demand_std_dev=100,
        avg_lead_time=7,
        min_safety_stock=0.25,  # Higher safety buffer
        max_safety_stock=0.50,
        container_sizes=(50, 100, 200),  # Larger containers
        z_score=1.96  # 97.5% service level
    )
    
    engine = GoogleAntigravity(seed=42, config=config)
    
    # Create sample high-demand data
    high_demand_data = pd.DataFrame({
        'node_id': [f'HD-{i:03d}' for i in range(1, 6)],
        'demand': [500, 750, 1200, 350, 900],
        'lead_time': [10, 14, 7, 5, 12],
        'product_name': ['Critical Part A', 'Essential Component B', 
                        'High-Volume Item C', 'Standard Part D', 'Key Module E']
    })
    
    results = engine.analyze_real_data(
        high_demand_data,
        demand_column='demand',
        lead_time_column='lead_time',
        node_id_column='node_id'
    )
    
    print("\n📊 High-Demand Analysis Results:")
    print(results[['node_id', 'product_name', 'demand_D', 'lead_time_L', 
                   'safety_stock_SS', 'kanban_cards_N', 'reorder_point_ROP']])
    
    print("\n💡 Insights:")
    print(f"   Average Kanban Cards Required: {results['kanban_cards_N'].mean():.1f}")
    print(f"   Average Reorder Point: {results['reorder_point_ROP'].mean():.0f} units")
    print(f"   Highest ROP Item: {results.loc[results['reorder_point_ROP'].idxmax(), 'product_name']}")


def example_3_comparative_analysis():
    """Example 3: Compare different scenarios."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Scenario Comparison (Current vs. Optimized)")
    print("=" * 70)
    
    # Sample data
    inventory_data = pd.DataFrame({
        'node_id': [f'ITEM-{i:02d}' for i in range(1, 6)],
        'demand': [200, 350, 150, 500, 275],
        'lead_time': [7, 5, 3, 10, 6]
    })
    
    scenarios = {
        'Current State': PhysicsConfig(avg_lead_time=7, min_safety_stock=0.20, max_safety_stock=0.30),
        'Optimized': PhysicsConfig(avg_lead_time=4, min_safety_stock=0.15, max_safety_stock=0.25),
        'Worst Case': PhysicsConfig(avg_lead_time=12, min_safety_stock=0.30, max_safety_stock=0.50)
    }
    
    print("\n📊 Scenario Comparison:")
    print("-" * 70)
    
    for scenario_name, config in scenarios.items():
        engine = GoogleAntigravity(seed=42, config=config)
        results = engine.analyze_real_data(
            inventory_data,
            demand_column='demand',
            lead_time_column='lead_time',
            node_id_column='node_id'
        )
        
        print(f"\n{scenario_name}:")
        print(f"   Avg Kanban Cards: {results['kanban_cards_N'].mean():.1f}")
        print(f"   Avg Reorder Point: {results['reorder_point_ROP'].mean():.0f}")
        print(f"   Total System Capacity: {(results['kanban_cards_N'] * results['container_capacity_C']).sum():,.0f} units")


def example_4_batch_processing():
    """Example 4: Process multiple files."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Batch Processing Multiple Data Files")
    print("=" * 70)
    
    engine = GoogleAntigravity()
    
    # Simulate multiple department data
    departments = {
        'Electronics': pd.DataFrame({
            'node_id': ['E001', 'E002', 'E003'],
            'demand': [300, 250, 400],
            'lead_time': [5, 4, 6]
        }),
        'Hardware': pd.DataFrame({
            'node_id': ['H001', 'H002', 'H003'],
            'demand': [150, 200, 180],
            'lead_time': [3, 4, 3]
        }),
        'Manufacturing': pd.DataFrame({
            'node_id': ['M001', 'M002', 'M003'],
            'demand': [500, 600, 450],
            'lead_time': [8, 10, 7]
        })
    }
    
    print("\n📊 Processing Multiple Departments:")
    
    all_results = []
    for dept_name, dept_data in departments.items():
        results = engine.analyze_real_data(
            dept_data,
            demand_column='demand',
            lead_time_column='lead_time',
            node_id_column='node_id'
        )
        results['department'] = dept_name
        all_results.append(results)
        
        print(f"\n{dept_name} Department:")
        print(f"   Items: {len(results)}")
        print(f"   Total Kanban Cards: {results['kanban_cards_N'].sum()}")
        print(f"   Avg Reorder Point: {results['reorder_point_ROP'].mean():.0f}")
    
    # Combine all results
    combined = pd.concat(all_results, ignore_index=True)
    print(f"\n✅ Total items processed: {len(combined)}")
    print(f"✅ Total Kanban cards across all departments: {combined['kanban_cards_N'].sum()}")


def main():
    """Run all examples."""
    print("\n⚡ Kanban Physics Engine - Real Data Examples")
    print("=" * 70)
    print("Demonstrating real-world usage with actual inventory data")
    print("=" * 70)
    
    # Run examples
    example_1_basic_analysis()
    example_2_custom_configuration()
    example_3_comparative_analysis()
    example_4_batch_processing()
    
    print("\n" + "=" * 70)
    print("✅ All examples completed!")
    print("=" * 70)
    print("\n💡 Next Steps:")
    print("   1. Replace example data with your actual inventory CSV files")
    print("   2. Adjust PhysicsConfig parameters to match your environment")
    print("   3. Use analyze_real_data() or load_and_analyze_csv() methods")
    print("   4. Export results and implement Kanban recommendations")
    print("\n📚 See USAGE_GUIDE.md for detailed documentation")
    print("=" * 70)


if __name__ == "__main__":
    main()
