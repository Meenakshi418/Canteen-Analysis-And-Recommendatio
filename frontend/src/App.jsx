import { useEffect, useState } from "react";
import "./App.css";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [summary, setSummary] = useState(null);
  const [topItems, setTopItems] = useState([]);
  const [wasteData, setWasteData] = useState([]);
  const [trendData, setTrendData] = useState([]);
  const [clusters, setClusters] = useState([]);
  const [apriori, setApriori] = useState(null);

  const [error, setError] = useState(null);

  const [demandResult, setDemandResult] = useState(null);

  /*
   * Existing prediction form.
   * The backend expects all 8 of these fields,
   * so they are kept unchanged.
   */
  const [demandForm, setDemandForm] = useState({
    students_count: "",
    quantity_prepared: "",
    price: "",
    day: "",
    meal_time: "",
    category: "",
    weather: "",
    special_event: ""
  });

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [
          summaryResponse,
          topItemsResponse,
          wasteResponse,
          trendsResponse,
          clustersResponse,
          aprioriResponse
        ] = await Promise.all([
          fetch(`${API_URL}/analytics/summary`),
          fetch(`${API_URL}/analytics/top_items`),
          fetch(`${API_URL}/analytics/waste`),
          fetch(`${API_URL}/analytics/trends`),
          fetch(`${API_URL}/mining/clusters`),
          fetch(`${API_URL}/mining/apriori`)
        ]);

        if (
          !summaryResponse.ok ||
          !topItemsResponse.ok ||
          !wasteResponse.ok ||
          !trendsResponse.ok ||
          !clustersResponse.ok ||
          !aprioriResponse.ok
        ) {
          throw new Error("One or more API requests failed");
        }

        const summaryData = await summaryResponse.json();
        const topItemsData = await topItemsResponse.json();
        const wasteResponseData = await wasteResponse.json();
        const trendsResponseData = await trendsResponse.json();
        const clustersData = await clustersResponse.json();
        const aprioriData = await aprioriResponse.json();

        setSummary(summaryData);
        setTopItems(topItemsData.top_items);
        setWasteData(wasteResponseData.total_waste_per_food_item);
        setClusters(clustersData.clusters);
        setApriori(aprioriData);

        const formattedTrends = Object.entries(
          trendsResponseData.total_quantity_sold_per_day
        ).map(([date, quantity]) => ({
          date,
          quantity
        }));

        setTrendData(formattedTrends);

      } catch (error) {
        console.error(error);
        setError(error.message);
      }
    }

    loadDashboard();
  }, []);

  function updateDemandForm(event) {
    setDemandForm({
      ...demandForm,
      [event.target.name]: event.target.value
    });

    // Remove old prediction when the user changes an input
    setDemandResult(null);
  }

  /*
   * Existing working prediction logic.
   * Do not change the parameters because the backend
   * prediction endpoint expects these exact fields.
   */
  async function predictDemand(event) {
    event.preventDefault();

    const params = new URLSearchParams(demandForm);

    try {
      const response = await fetch(
        `${API_URL}/prediction/demand?${params.toString()}`
      );

      if (!response.ok) {
        throw new Error("Demand prediction failed");
      }

      const data = await response.json();

      setDemandResult(data.predicted_quantity_sold);

    } catch (error) {
      console.error(error);
      setError(error.message);
    }
  }

  if (error) {
    return (
      <div className="dashboard">
        <h2>API Error</h2>
        <p>{error}</p>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="dashboard">
        <h2>Loading SmartCanteen...</h2>
      </div>
    );
  }

  return (
    <div className="dashboard">

      {/* HEADER */}

      <header className="dashboard-header">
        <h1>SmartCanteen</h1>
        <p>
          Demand Prediction and Food Waste Analytics
        </p>
      </header>


      {/* OVERVIEW */}

      <section>
        <h2 className="section-title">
          Overview
        </h2>

        <div className="card-container">

          <div className="summary-card">
            <h3>Total Quantity Sold</h3>

            <p className="big-number">
              {summary.total_quantity_sold}
            </p>
          </div>

          <div className="summary-card">
            <h3>Total Food Waste</h3>

            <p className="big-number">
              {summary.total_food_waste}
            </p>
          </div>

          <div className="summary-card">
            <h3>Average Rating</h3>

            <p className="big-number">
              {summary.average_rating.toFixed(2)}
            </p>
          </div>

        </div>
      </section>


      {/* SALES ANALYTICS */}

      <section>
        <h2 className="section-title">
          Sales Analytics
        </h2>

        <div className="chart-card">

          <h3>Top Selling Food Items</h3>

          <ResponsiveContainer
            width="100%"
            height={400}
          >
            <BarChart data={topItems}>

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis
                dataKey="food_item"
                angle={-45}
                textAnchor="end"
                interval={0}
                height={100}
              />

              <YAxis />

              <Tooltip />

              <Bar dataKey="quantity" />

            </BarChart>
          </ResponsiveContainer>

        </div>


        <div className="chart-card">

          <h3>Food Waste by Item</h3>

          <ResponsiveContainer
            width="100%"
            height={400}
          >
            <BarChart data={wasteData}>

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis
                dataKey="food_item"
                angle={-45}
                textAnchor="end"
                interval={0}
                height={100}
              />

              <YAxis />

              <Tooltip />

              <Bar dataKey="waste" />

            </BarChart>
          </ResponsiveContainer>

        </div>


        <div className="chart-card">

          <h3>Daily Quantity Sold</h3>

          <ResponsiveContainer
            width="100%"
            height={400}
          >
            <LineChart data={trendData}>

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis dataKey="date" />

              <YAxis />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="quantity"
              />

            </LineChart>
          </ResponsiveContainer>

        </div>

      </section>


      {/* DEMAND PREDICTION */}

      <section>

        <h2 className="section-title">
          Demand Prediction
        </h2>

        <div className="form-grid">

          <form
            className="form-card"
            onSubmit={predictDemand}
          >

            <h3>
              Predict Quantity Sold
            </h3>

            <p className="form-description">
              Enter the expected conditions to estimate
              how many portions are likely to be sold.
            </p>


            {/* STUDENTS COUNT */}

            <label htmlFor="students_count">
              Expected Number of Students
            </label>

            <input
              id="students_count"
              name="students_count"
              type="number"
              min="1"
              placeholder="Example: 300"
              value={demandForm.students_count}
              onChange={updateDemandForm}
              required
            />


            {/* QUANTITY PREPARED */}

            <label htmlFor="quantity_prepared">
              Quantity Prepared
            </label>

            <input
              id="quantity_prepared"
              name="quantity_prepared"
              type="number"
              min="1"
              placeholder="Example: 120 portions"
              value={demandForm.quantity_prepared}
              onChange={updateDemandForm}
              required
            />


            {/* PRICE */}

            <label htmlFor="price">
              Food Price
            </label>

            <input
              id="price"
              name="price"
              type="number"
              min="0"
              step="0.01"
              placeholder="Example: ₹30"
              value={demandForm.price}
              onChange={updateDemandForm}
              required
            />


            {/* DAY */}

            <label htmlFor="day">
              Day
            </label>

            <select
              id="day"
              name="day"
              value={demandForm.day}
              onChange={updateDemandForm}
              required
            >

              <option value="">
                Select a day
              </option>

              <option value="Monday">
                Monday
              </option>

              <option value="Tuesday">
                Tuesday
              </option>

              <option value="Wednesday">
                Wednesday
              </option>

              <option value="Thursday">
                Thursday
              </option>

              <option value="Friday">
                Friday
              </option>

              <option value="Saturday">
                Saturday
              </option>

              <option value="Sunday">
                Sunday
              </option>

            </select>


            {/* MEAL TIME */}

            <label htmlFor="meal_time">
              Meal Time
            </label>

            <select
              id="meal_time"
              name="meal_time"
              value={demandForm.meal_time}
              onChange={updateDemandForm}
              required
            >

              <option value="">
                Select meal time
              </option>

              <option value="Breakfast">
                Breakfast
              </option>

              <option value="Lunch">
                Lunch
              </option>

              <option value="Evening">
                Evening
              </option>

            </select>


            {/* CATEGORY */}

            <label htmlFor="category">
              Food Category
            </label>

            <select
              id="category"
              name="category"
              value={demandForm.category}
              onChange={updateDemandForm}
              required
            >

              <option value="">
                Select food category
              </option>

              <option value="Snacks">
                Snacks
              </option>

              <option value="Meals">
                Meals
              </option>

            </select>


            {/* WEATHER */}

            <label htmlFor="weather">
              Weather
            </label>

            <select
              id="weather"
              name="weather"
              value={demandForm.weather}
              onChange={updateDemandForm}
              required
            >

              <option value="">
                Select weather
              </option>

              <option value="Sunny">
                Sunny
              </option>

              <option value="Cloudy">
                Cloudy
              </option>

              <option value="Rainy">
                Rainy
              </option>

            </select>


            {/* SPECIAL EVENT */}

            <label htmlFor="special_event">
              Special Event
            </label>

            <select
              id="special_event"
              name="special_event"
              value={demandForm.special_event}
              onChange={updateDemandForm}
              required
            >

              <option value="">
                Select event status
              </option>

              <option value="Yes">
                Yes
              </option>

              <option value="No">
                No
              </option>

            </select>


            {/* PREDICT BUTTON */}

            <button type="submit">
              Predict Quantity
            </button>


            {/* RESULT */}

            {demandResult !== null && (

              <div className="prediction-result">

                <p>
                  Predicted Quantity Sold
                </p>

                <strong>
                  {demandResult} portions
                </strong>

              </div>

            )}

          </form>

        </div>

      </section>


      {/* CLUSTERING */}

      <section>

        <h2 className="section-title">
          Customer and Canteen Patterns
        </h2>

        <div className="chart-card">

          <h3>Cluster Analysis</h3>

          <ResponsiveContainer
            width="100%"
            height={400}
          >
            <BarChart data={clusters}>

              <CartesianGrid
                strokeDasharray="3 3"
              />

              <XAxis dataKey="cluster" />

              <YAxis />

              <Tooltip />

              <Bar dataKey="quantity_sold" />

            </BarChart>
          </ResponsiveContainer>

        </div>


        <div className="cluster-grid">

          {clusters.map((cluster) => (

            <div
              className="cluster-card"
              key={cluster.cluster}
            >

              <h3>
                Cluster {cluster.cluster}
              </h3>

              <p>
                Average Sales:{" "}
                {cluster.quantity_sold}
              </p>

              <p>
                Average Waste:{" "}
                {cluster.food_waste}
              </p>

              <p>
                Students:{" "}
                {cluster.students_count}
              </p>

              <p>
                Rating:{" "}
                {cluster.rating}
              </p>

            </div>

          ))}

        </div>

      </section>


      {/* APRIORI */}

      <section>

        <h2 className="section-title">
          Food Item Associations
        </h2>

        {apriori && (

          <div className="chart-card">

            <h3>
              Association Rules
            </h3>

            {apriori.association_rules.map(
              (rule, index) => (

                <div
                  className="rule"
                  key={index}
                >

                  <strong>
                    {rule.antecedents.join(", ")}
                    {" → "}
                    {rule.consequents.join(", ")}
                  </strong>

                  <p>

                    Support:{" "}
                    {(rule.support * 100).toFixed(2)}
                    %

                    {" | "}

                    Confidence:{" "}
                    {(rule.confidence * 100).toFixed(2)}
                    %

                    {" | "}

                    Lift:{" "}
                    {rule.lift.toFixed(2)}

                  </p>

                </div>

              )
            )}

          </div>

        )}

      </section>

    </div>
  );
}

export default App;