# 📘 Kanban Physics Engine - Usage Guide

## 🎯 Purpose

The Kanban Physics Engine is a production-ready tool for analyzing and optimizing Kanban systems using Six Sigma Yellow Belt methodology (Pages 297-308). This engine transforms real operational data into actionable insights for inventory management, supply chain optimization, and process improvement.

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Purmamarca/kanban-physics-engine.git
cd kanban-physics-engine

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from social_physics_engine.generate_data import GoogleAntigravity
import pandas as pd

# Initialize the engine
engine = GoogleAntigravity(seed=42)

# Option 1: Generate simulated data for testing
df = engine.generate_complete_dataset(n_nodes=200)

# Option 2: Load your real data
real_data = pd.read_csv('your_data.csv')
analyzed_data = engine.analyze_real_data(real_data)

# Export results
analyzed_data.to_csv('kanban_analysis_results.csv', index=False)
```

---

## 📊 Working with Real Data

### Input Data Format

Your CSV file should contain the following columns:

| Column Name                     | Type    | Description                    | Example   |
| ------------------------------- | ------- | ------------------------------ | --------- |
| `node_id` or `product_id`       | int/str | Unique identifier              | "SKU-001" |
| `demand` or `avg_demand`        | int     | Average daily demand           | 250       |
| `lead_time`                     | int     | Replenishment lead time (days) | 5         |
| `safety_stock` (optional)       | float   | Safety stock percentage (0-1)  | 0.20      |
| `container_capacity` (optional) | int     | Container size                 | 50        |

**Minimal Example CSV:**

```csv
node_id,demand,lead_time
SKU-001,250,5
SKU-002,180,3
SKU-003,420,7
```

### Loading and Analyzing Real Data

```python
from social_physics_engine.generate_data import GoogleAntigravity
import pandas as pd

# Load your data
data = pd.read_csv('inventory_data.csv')

# Initialize engine
engine = GoogleAntigravity()

# Analyze and calculate Kanban metrics
results = engine.analyze_real_data(
    data=data,
    demand_column='demand',
    lead_time_column='lead_time',
    node_id_column='node_id'
)

# View results
print(results[['node_id', 'kanban_cards_N', 'reorder_point_ROP']])

# Export
results.to_csv('kanban_recommendations.csv', index=False)
```

---

## 🔧 Advanced Configuration

### Custom Physics Parameters

```python
from social_physics_engine.generate_data import GoogleAntigravity, PhysicsConfig

# Define custom configuration
config = PhysicsConfig(
    avg_demand=300,              # Higher baseline demand
    demand_std_dev=75,           # More variability
    avg_lead_time=7,             # Longer lead times
    min_safety_stock=0.15,       # Minimum 15% buffer
    max_safety_stock=0.40,       # Maximum 40% buffer
    container_sizes=(25, 75, 150),  # Custom container sizes
    z_score=1.96                 # 97.5% service level
)

# Initialize with custom config
engine = GoogleAntigravity(seed=42, config=config)
```

### Batch Processing Multiple Files

```python
import glob
import pandas as pd
from social_physics_engine.generate_data import GoogleAntigravity

engine = GoogleAntigravity()

# Process all CSV files in a directory
for file in glob.glob('data/*.csv'):
    print(f"Processing {file}...")
    data = pd.read_csv(file)
    results = engine.analyze_real_data(data)

    # Save with descriptive name
    output_name = file.replace('.csv', '_analyzed.csv')
    results.to_csv(output_name, index=False)
    print(f"✅ Saved to {output_name}")
```

---

## 📈 Understanding the Output

### Key Metrics Explained

#### 1. **Kanban Cards (N)**

- **Formula:** `N = (D × L × (1 + SS)) / C`
- **Meaning:** Number of Kanban cards needed in the system
- **Action:** This is the number of containers/cards to create

#### 2. **Reorder Point (ROP)**

- **Formula:** `ROP = D × L × (1 + SS)`
- **Meaning:** Inventory level that triggers replenishment
- **Action:** When inventory hits this level, order more

#### 3. **Safety Stock (SS)**

- **Meaning:** Buffer percentage against variability
- **Range:** Typically 10-30% (0.10-0.30)
- **Action:** Higher SS = more protection against stockouts

### Example Output Interpretation

```
node_id: SKU-001
demand_D: 250 units/day
lead_time_L: 5 days
safety_stock_SS: 0.20 (20%)
container_capacity_C: 50 units
kanban_cards_N: 30 cards
reorder_point_ROP: 1500 units
```

**What this means:**

- You need **30 Kanban cards** in circulation
- Each card represents **50 units** (container capacity)
- When inventory drops to **1500 units**, trigger replenishment
- Total system capacity: 30 × 50 = **1500 units**

---

## 🎯 Real-World Use Cases

### Use Case 1: Manufacturing Inventory Optimization

```python
# Load production data
production_data = pd.read_csv('manufacturing_parts.csv')

# Analyze
engine = GoogleAntigravity()
results = engine.analyze_real_data(production_data)

# Find items needing most Kanban cards
high_demand = results.nlargest(10, 'kanban_cards_N')
print("Top 10 items by Kanban card requirement:")
print(high_demand[['node_id', 'demand_D', 'kanban_cards_N']])
```

### Use Case 2: Supply Chain Analysis

```python
# Custom config for supply chain
config = PhysicsConfig(
    avg_lead_time=10,        # Longer supply chain
    min_safety_stock=0.25,   # Higher safety buffer
    max_safety_stock=0.50
)

engine = GoogleAntigravity(config=config)
results = engine.analyze_real_data(supply_chain_data)

# Identify high-risk items (high ROP)
high_risk = results[results['reorder_point_ROP'] > 5000]
high_risk.to_csv('high_risk_items.csv', index=False)
```

### Use Case 3: Simulation and What-If Analysis

```python
# Simulate different scenarios
scenarios = {
    'current': PhysicsConfig(avg_lead_time=5),
    'optimized': PhysicsConfig(avg_lead_time=3),
    'worst_case': PhysicsConfig(avg_lead_time=10)
}

for scenario_name, config in scenarios.items():
    engine = GoogleAntigravity(config=config)
    results = engine.generate_complete_dataset(n_nodes=100)

    print(f"\n{scenario_name.upper()} Scenario:")
    print(f"Avg Kanban Cards: {results['kanban_cards_N'].mean():.1f}")
    print(f"Avg Reorder Point: {results['reorder_point_ROP'].mean():.1f}")
```

---

## 🔍 Troubleshooting

### Common Issues

**Issue:** "Column not found" error

```python
# Solution: Specify exact column names
results = engine.analyze_real_data(
    data=df,
    demand_column='daily_demand',  # Your actual column name
    lead_time_column='lead_days'
)
```

**Issue:** Negative demand values

```python
# The engine automatically handles this with np.abs()
# But you can pre-clean your data:
data['demand'] = data['demand'].abs()
```

**Issue:** Missing safety stock values

```python
# The engine will calculate defaults if not provided
# Or specify manually:
data['safety_stock_SS'] = 0.20  # 20% for all items
```

---

## 📚 Six Sigma Compliance

This engine strictly follows Six Sigma Yellow Belt Kanban methodology:

- **Page 297:** Core Kanban formula `N = (D × L × (1 + SS)) / C`
- **Page 300:** Rule 2 - Standardized container sizes
- **Page 301:** Safety stock as variability hedge

All calculations are empirically proven and industry-standard.

---

## 🤝 Support and Contribution

### Getting Help

- Review this guide thoroughly
- Check the README.md for technical details
- Examine the example code in `social_physics_engine/generate_data.py`

### Contributing

- Maintain Six Sigma compliance
- Preserve vectorized performance
- Add comprehensive tests
- Update documentation

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🔗 Additional Resources

- Six Sigma Yellow Belt Certification Material (Pages 297-308)
- Kanban methodology and visual management
- Lean manufacturing principles
- Statistical process control (SPC)

---

**⚡ Built for production. Proven by Six Sigma. Ready for your real data.**
