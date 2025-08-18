from flask import Flask, render_template, request
import numpy as np
import plotly.graph_objs as go
import plotly.offline as plot

app = Flask(__name__)

def simulate_sir(population, beta, gamma, days):
    S = [population - 1]  # Susceptible
    I = [1]               # Infected (start with 1 case)
    R = [0]               # Recovered
    
    for t in range(1, days):
        new_infected = beta * S[-1] * I[-1] / population
        new_recovered = gamma * I[-1]
        
        S.append(S[-1] - new_infected)
        I.append(I[-1] + new_infected - new_recovered)
        R.append(R[-1] + new_recovered)
    
    return list(range(days)), S, I, R

@app.route("/", methods=["GET", "POST"])
def index():
    graph = None
    if request.method == "POST":
        population = int(request.form["population"])
        beta = float(request.form["beta"])
        gamma = float(request.form["gamma"])
        days = int(request.form["days"])

        t, S, I, R = simulate_sir(population, beta, gamma, days)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=t, y=S, mode="lines", name="Susceptible", hovertemplate="Day %{x}: %{y:.0f}"))
        fig.add_trace(go.Scatter(x=t, y=I, mode="lines", name="Infected", hovertemplate="Day %{x}: %{y:.0f}"))
        fig.add_trace(go.Scatter(x=t, y=R, mode="lines", name="Recovered", hovertemplate="Day %{x}: %{y:.0f}"))

        fig.update_layout(
            title="Epidemic Spread Simulation (SIR Model)",
            xaxis_title="Days",
            yaxis_title="Number of People",
            template="plotly_dark"
        )

        graph = plot.plot(fig, output_type="div")

    return render_template("index.html", graph=graph)

if __name__ == "__main__":
    app.run(debug=True)
