// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import LoadingSpinner from './LoadingSpinner';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

function App() {
  const [url, setUrl] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // Show spinner
    try {
      const response = await axios.post('http://localhost:5000/analyze_comments', {
        url,
        username,
        password
      });
      setResult(response.data);
    } catch (error) {
      console.error('Error fetching comments:', error);
    } finally {
      setLoading(false); // Hide spinner
    }
  };

  const chartData = {
    labels: ['Hate Comments', 'Non-Hate Comments'],
    datasets: [
      {
        data: [result?.hate_comments || 0, result?.non_hate_comments || 0],
        backgroundColor: ['rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)'],
        borderColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)'],
        borderWidth: 1
      }
    ]
  };

  const barChartData = {
    labels: ['Total Comments'],
    datasets: [
      {
        label: 'Comments Count',
        data: [result?.total_comments || 0],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1
      }
    ]
  };

  return (
    <div className="App">
      <header>
        <h1>Facebook Comments Analyzer</h1>
      </header>
      <main>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Facebook Post URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
          />
          <input
            type="text"
            placeholder="Facebook Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Facebook Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Analyze Comments</button>
        </form>
        {loading ? (
          <LoadingSpinner />
        ) : result ? (
          <div className="results">
            <h2>Results:</h2>
            <p><strong>Total Comments:</strong> {result.total_comments}</p>
            <p><strong>Hate Comments:</strong> {result.hate_comments}</p>
            <p><strong>Non-Hate Comments:</strong> {result.non_hate_comments}</p>
            <p><strong>Hate Percentage:</strong> {result.hate_percentage.toFixed(2)}%</p>
            <div className="chart-container">
              <h3>Comments Distribution</h3>
              <Pie data={chartData} />
              <h3>Total Comments</h3>
              <Bar data={barChartData} />
            </div>
            <div className="comments-list">
              <h3>Comments:</h3>
              <ul>
                {result.comments.map((comment, index) => (
                  <li key={index}>
                    <strong>{comment.name}:</strong> {comment.comment}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ) : null}
      </main>
    </div>
  );
}

export default App;
