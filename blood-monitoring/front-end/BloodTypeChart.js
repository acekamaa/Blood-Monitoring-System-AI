// src/BloodTypeChart.js
import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

function BloodTypeChart({ data }) {
  const chartData = {
    labels: data.map(item => item.blood_type),
    datasets: [{
      data: data.map(item => item.count),
      backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF', '#E7E9ED'],
    }],
  };

  return <Pie data={chartData} />;
}

export default BloodTypeChart;