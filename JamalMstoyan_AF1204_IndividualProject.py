# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo>=0.23.1",
#     "pandas==3.0.2",
#     "plotly==6.7.0",
# ]
# ///

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell
def _(
    cogs_slider,
    fig_comparison,
    fig_full,
    fig_profit,
    fig_scenarios,
    logistics_slider,
    markup_slider,
    metrics_block,
    mo,
    profit_summary,
    selected_cogs,
    selected_logistics,
    selected_markup,
):
    home_tab = mo.md("""
    # Jamal Mstoyan

    ### Accounting & Finance Student | Entrepreneur

    ---

    ## Profile

    I am an Accounting and Finance student with an interest in financial analysis, profitability, and business decision-making.

    Alongside my studies, I have practical experience in retail. Since 2024, I have been operating as an individual entrepreneur and developing grocery stores in Kazakhstan. This gave me hands-on exposure to pricing, cost control, and day-to-day business decisions.

    ---

    ## Education

    **Kazakhstan, №5 Gymnasium School of Rudny**  
    2013–2023

    **Abbey College Cambridge (Business Pathway)**  
    2023–2025

    **Accounting & Finance**  
    Bayes Business School, City St George’s, University of London  
    Current programme

    ---

    ## Experience

    **Individual Entrepreneur**  
    Since 2024

    - Managing grocery retail operations in Kazakhstan  
    - Working with pricing, costs, and business performance  
    - Making practical commercial decisions  

    ---

    ## Leadership Experience

    **School President (Rudny)**

    Elected by students to represent the school. This helped me develop communication, responsibility, and decision-making skills.

    ---

    ## Interests

    - Financial analysis  
    - Profitability  
    - Cost structure  
    - Retail business  
    - Data-based decision-making  

    ---

    ## Purpose of This Page

    This page shows a simple financial model of a retail business. It focuses on how markup and costs affect profit, using interactive inputs and charts.
    """)

    project_tab_intro = mo.md("""
    # Retail Profitability Analysis

    This section looks at how markup and costs affect revenue and profit.

    You can change the inputs and see how the results move.
    """)

    skills_tab = mo.md("""
    # Skills Demonstrated

    ## Technical

    - Python for financial calculations  
    - Interactive inputs (sliders)  
    - Plotly charts  

    ## Analytical

    - Profit calculation  
    - Cost structure understanding  
    - Scenario comparison  

    ## Communication

    - Presenting results clearly  
    - Turning numbers into visual output  
    """)

    contact_tab = mo.md("""
    # Contact

    Email: Jamal.Mstoyan@bayes.city.ac.uk  

    London, United Kingdom
    """)

    break_even_markup = selected_logistics / selected_cogs
    break_even_status = "Profitable" if selected_markup > break_even_markup else "Below break-even"

    tabs = mo.ui.tabs({
        "Home": home_tab,

        "Profitability Analysis": mo.vstack([
            project_tab_intro,

            mo.md("""
    ## Financial Model

    Revenue = Cost of Goods × (1 + Markup)  
    Profit = Revenue − Costs − Logistics
    """),

            cogs_slider,
            markup_slider,
            logistics_slider,

            profit_summary,
            metrics_block,

            mo.md(f"""
    ## Break-even

    Break-even markup: **{break_even_markup:.1%}**  
    Current status: **{break_even_status}**
    """),

            mo.md("## Profit vs Markup"),
            mo.ui.plotly(fig_profit),

            mo.md("## Revenue, Costs, Profit"),
            mo.ui.plotly(fig_comparison),

            mo.md("## Scenario Comparison"),
            mo.ui.plotly(fig_scenarios),

            mo.md("## Full Sensitivity Analysis"),
            mo.ui.plotly(fig_full)
        ]),

        "Skills": skills_tab,
        "Contact": contact_tab
    })

    tabs
    return


@app.cell
def _():
    import marimo as mo


    return (mo,)


@app.cell
def _():
    import plotly.express as px
    import pandas as pd

    return pd, px


@app.cell
def _(mo):
    cogs_slider = mo.ui.slider(
        start=50_000,
        stop=400_000,
        step=10_000,
        value=200_000,
        label="Cost of goods sold (£)"
    )

    markup_slider = mo.ui.slider(
        start=0.05,
        stop=0.50,
        step=0.01,
        value=0.25,
        label="Markup (%)"
    )

    logistics_slider = mo.ui.slider(
        start=10_000,
        stop=100_000,
        step=5_000,
        value=40_000,
        label="Logistics cost (£)"
    )

    mo.vstack([
        cogs_slider,
        markup_slider,
        logistics_slider
    ])
    return cogs_slider, logistics_slider, markup_slider


@app.cell
def _(cogs_slider, logistics_slider, markup_slider, mo):
    selected_cogs = cogs_slider.value
    selected_markup = markup_slider.value
    selected_logistics = logistics_slider.value

    calculated_revenue = selected_cogs * (1 + selected_markup)
    calculated_total_costs = selected_cogs + selected_logistics
    calculated_profit = calculated_revenue - calculated_total_costs
    gross_margin = calculated_profit / calculated_revenue

    profit_summary = mo.md(f"""
    # Interactive Profit Analysis

    **Cost of goods sold:** £{selected_cogs:,.0f}  
    **Markup:** {selected_markup:.0%}  
    **Logistics cost:** £{selected_logistics:,.0f}  

    **Calculated revenue:** £{calculated_revenue:,.0f}  
    **Total costs:** £{calculated_total_costs:,.0f}  

    ## Estimated Profit: £{calculated_profit:,.0f}

    **Profit margin:** {gross_margin:.1%}
    """)

    profit_summary
    return (
        calculated_profit,
        calculated_revenue,
        calculated_total_costs,
        gross_margin,
        profit_summary,
        selected_cogs,
        selected_logistics,
        selected_markup,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Profit Sensitivity Chart

    The chart below shows how estimated profit changes as the markup percentage increases, while cost of goods sold and logistics cost remain fixed at the selected values.
    """)
    return


@app.cell
def _(mo, pd, px, selected_cogs, selected_logistics):
    markup_values = [i / 100 for i in range(5, 51)]

    profit_table = pd.DataFrame({
        "Markup": markup_values
    })

    profit_table["Revenue"] = selected_cogs * (1 + profit_table["Markup"])
    profit_table["Total Costs"] = selected_cogs + selected_logistics
    profit_table["Profit"] = profit_table["Revenue"] - profit_table["Total Costs"]
    profit_table["Markup Label"] = (profit_table["Markup"] * 100).round(0).astype(int).astype(str) + "%"

    fig_profit = px.line(
        profit_table,
        x="Markup",
        y="Profit",
        markers=True,
        title="Estimated Profit at Different Markup Levels",
        labels={
            "Markup": "Markup (%)",
            "Profit": "Estimated Profit (£)"
        }
    )

    fig_profit.update_traces(
        hovertemplate="Markup: %{x:.0%}<br>Profit: £%{y:,.0f}<extra></extra>"
    )

    fig_profit.update_layout(
        template="presentation",
        width=900,
        height=500
    )

    mo.ui.plotly(fig_profit)
    return (fig_profit,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Key Financial Metrics

    The key outputs below summarise the financial position under the selected pricing and cost assumptions.
    """)
    return


@app.cell
def _(
    calculated_profit,
    calculated_revenue,
    calculated_total_costs,
    gross_margin,
    mo,
    selected_cogs,
    selected_logistics,
    selected_markup,
):
    metrics_block = mo.md(f"""
    | Metric | Value |
    |---|---:|
    | Cost of goods sold | £{selected_cogs:,.0f} |
    | Markup | {selected_markup:.0%} |
    | Logistics cost | £{selected_logistics:,.0f} |
    | Calculated revenue | £{calculated_revenue:,.0f} |
    | Total costs | £{calculated_total_costs:,.0f} |
    | Estimated profit | £{calculated_profit:,.0f} |
    | Profit margin | {gross_margin:.1%} |
    """)

    metrics_block# Revenue, Costs, and Profit Comparison

    return (metrics_block,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Revenue, Costs, and Profit Comparison

    The chart below compares the main financial components generated by the selected scenario.
    """)
    return


@app.cell
def _(
    calculated_profit,
    calculated_revenue,
    calculated_total_costs,
    mo,
    pd,
    px,
):
    comparison_df = pd.DataFrame({
        "Category": ["Revenue", "Total Costs", "Profit"],
        "Amount": [calculated_revenue, calculated_total_costs, calculated_profit]
    })

    fig_comparison = px.bar(
        comparison_df,
        x="Category",
        y="Amount",
        title="Comparison of Revenue, Total Costs, and Profit",
        labels={"Amount": "Amount (£)", "Category": "Financial Measure"},
        text="Amount"
    )

    fig_comparison.update_traces(
        texttemplate="£%{y:,.0f}",
        textposition="outside"
    )

    fig_comparison.update_layout(
        template="presentation",
        width=900,
        height=500
    )

    mo.ui.plotly(fig_comparison)
    return (fig_comparison,)


@app.cell
def _(mo, pd, px, selected_cogs, selected_logistics):
    scenario_data = pd.DataFrame({
        "Scenario": ["Low Markup", "Medium Markup", "High Markup"],
        "Markup": [0.15, 0.25, 0.40]
    })

    scenario_data["Revenue"] = selected_cogs * (1 + scenario_data["Markup"])
    scenario_data["Total Costs"] = selected_cogs + selected_logistics
    scenario_data["Profit"] = scenario_data["Revenue"] - scenario_data["Total Costs"]

    fig_scenarios = px.bar(
        scenario_data,
        x="Scenario",
        y="Profit",
        color="Scenario",
        title="Profit Comparison Across Pricing Scenarios"
    )

    fig_scenarios.update_layout(template="presentation")

    mo.ui.plotly(fig_scenarios)
    return (fig_scenarios,)


@app.cell
def _(mo, pd, px, selected_cogs, selected_logistics):
    markup_range = [i / 100 for i in range(0, 51)]

    df_full = pd.DataFrame({
        "Markup": markup_range
    })

    df_full["Revenue"] = selected_cogs * (1 + df_full["Markup"])
    df_full["Total Costs"] = selected_cogs + selected_logistics
    df_full["Profit"] = df_full["Revenue"] - df_full["Total Costs"]

    fig_full = px.line(
        df_full,
        x="Markup",
        y="Profit",
        title="Profit vs Markup (Full Sensitivity Analysis)"
    )

    fig_full.update_layout(template="presentation")

    mo.ui.plotly(fig_full)
    return (fig_full,)


if __name__ == "__main__":
    app.run()
