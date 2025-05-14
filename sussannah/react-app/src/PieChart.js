import React from "react";
import { Pie } from "react-chartjs-2";

const defaultColors = ['#9A99D7', '#C0CDED', '#B460E7'];

function PieChart({ chartData }) {

  const data = {
    ...chartData,
    datasets: chartData.datasets.map(ds => ({
      ...ds,
      backgroundColor: defaultColors
    }))
  };

  return (
    <Pie
      data={data}
      options={{
        plugins: {
          legend: {
            labels: {
              color: "black"
            }
          }
        }
      }}
    />
  );
}

export default PieChart;
