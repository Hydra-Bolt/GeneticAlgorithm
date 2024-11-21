# Aladdin's Backpack Optimizer

A genetic algorithm solution for optimizing item selection in a backpack considering weight limits, item values, and fragility.

## Problem Description

The challenge is to help Aladdin select items for his backpack while:
- Staying within a maximum weight limit
- Maximizing the total value of selected items
- Minimizing the impact of fragile items
- Handling binary decisions (take/leave) for each item

## Solution

The project implements a genetic algorithm with:
- Binary string representation for item selection
- Tournament selection for parent choice
- Single-point crossover
- Random mutation
- Fitness evaluation based on value minus fragility
- GUI interface for parameter tuning

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Hydra-Bolt/GeneticAlgorithm.git
cd GeneticAlgorithm
```

2. Install dependencies:
```bash
pip install tkinter
```

## Usage

Run the GUI application:
```bash
python gui.py
```

Adjust parameters:
- Number of Items
- Generations
- Backpack Size
- Weight Range
- Value Range
- Fragility Range
- Mutation Probability

Click "Run Optimization" to find the optimal solution.

## Requirements
- Python 3.6+
- tkinter