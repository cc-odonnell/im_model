# im_model
Inventory Management Statistical Modeling


To develop this framework, I generated synthetic demand and lead time data, then created a simulation that modeled inventory behaviors over time. Using this simulated data, I conducted a factorial design analysis, testing various combinations of R and Q to map out the feasible solution space. This allowed me to explore how different reorder points and order quantities affected outcomes across different inventory configurations.

The focus of my analysis was on comparing the optimal solutions given by three common methods: cut-off thresholds, linear programming, and multi-objective optimization (Pareto Optimality).

**Cut-Off Thresholds**:
**Example**: Of the solutions with a fill rate greater than 95%, which one minimizes the number of deliveries?
**Pros**: Easy to understand and simple to program. The process stops at the first feasible solution that meets the fill rate threshold, then identifies the scenario with the fewest deliveries.
**Cons**: This approach may miss better solutions where a slightly lower fill rate (e.g., 95.1%) might reduce deliveries significantly—achieving a more balanced outcome.

**Linear Programming**:
**Example**: Define an objective function to minimize total deliveries and cubic space used, subject to the constraint that fill rate must exceed 95%.
**Pros**: Best if you know the relative importance of each objective (e.g., fill rate vs. delivery count). LP provides a clear, optimal solution without the need to evaluate many trade-offs.
**Cons**: It’s more suited to simpler problems where trade-offs are well understood. Adjusting weights can be tricky if priorities shift.

**Multi-Objective Optimization (Pareto Optimality)**:
**Example**: Which solutions provide the best balance between fill rate and total deliveries?
**Pros**: Ideal for exploring trade-offs between competing objectives before making a decision. It’s perfect for complex scenarios where objectives are difficult to prioritize, offering a range of optimal solutions.
**Cons**: More computationally intensive, but it provides a broader view of possible outcomes, making it especially valuable when discussing options with stakeholders.
