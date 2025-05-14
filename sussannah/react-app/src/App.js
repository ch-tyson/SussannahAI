import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";
import PieChart from "./PieChart";
import InfoCard from "./InfoCard";
import {
  Chart,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
Chart.register(
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  // new line start
  const scanOption = ["Sentiment", "Spam", "Summary"];
  const [checkedState, setCheckedState] = useState(
    new Array(scanOption.length).fill(false)
  );

  const [result, setResultData] = useState(null);
  const [sentimentData, setSentimentData] = useState(null);
  const [spamData, setSpamData] = useState(null);

  let initialState = {
    name: "Enter your text here",
    options: [],
  };
  const [analysisForm, setAnalysisForm] = useState(initialState);
  const textareaRef = useRef(null);

  const chartOptions = {
    plugins: {
      legend: {
        labels: {
          font: {
            family: "'Outfit', sans-serif",
            size: 14
          }
        }
      }
    }
  };

  function getData(e) {
    e.preventDefault();
    const API_URL = process.env.REACT_APP_API_URL || 'https://sussannahai-1.onrender.com';
    console.log('Sending request to:', API_URL);
    console.log('Request data:', analysisForm);
    
    axios({
      method: "post",
      url: `${API_URL}/spam`,
      data: JSON.stringify(analysisForm),
      headers: { "Content-Type": "application/json" },
    })
      .then((response) => {
        console.log('Response received:', response.data);
        const res = response.data;
        setResultData({
          paragraph: res.summary ? res.summary : null,
          options: [
            res.sentiment ? res.sentiment : null,
            res.spam ? res.spam : null,
          ],
          sentimentValue: res.sentimentValue,
        });
        if (res.sentimentValue)
          setSentimentData({
            labels: ["Negative", "Positive", "Neutral"],
            datasets: [
              {
                label: "Sentiment analysis",
                data: res.sentimentValue,
                backgroundColor: ["#e9ecef", "#aca8e3", "#d4d1f3"],
                borderColor: "#aca8e3",
                borderWidth: 2,
              },
            ],
          });
        else setSentimentData(null);
        if (res.spamValue)
          setSpamData({
            labels: ["Spam", "Not spam"],
            datasets: [
              {
                label: "Spam analysis",
                data: res.spamValue,
                backgroundColor: ["#e9ecef", "#aca8e3"],
                borderColor: "#aca8e3",
                borderWidth: 2,
              },
            ],
          });
        else setSpamData(null);
      })
      .catch((error) => {
        console.error('Error details:', {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status,
          headers: error.response?.headers
        });
        
        // Show error to user
        setResultData({
          paragraph: "Error: Could not analyze text. Please try again.",
          options: [null, null],
          sentimentValue: null
        });
      });
  }
  //end of new line

  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = Math.min(textarea.scrollHeight, 300) + 'px';
    }
  };

  const onChangeHandler = (event) => {
    const { name, value } = event;
    setAnalysisForm((prev) => {
      return { ...prev, [name]: value };
    });
    adjustTextareaHeight();
  };

  useEffect(() => {
    adjustTextareaHeight();
  }, [analysisForm.paragraph]);

  const handleOnChange = (position) => {
    const updatedCheckedState = checkedState.map((item, index) =>
      index === position ? !item : item
    );

    setCheckedState(updatedCheckedState);

    setAnalysisForm((prev) => {
      let choices = [];

      for (let i = 0; i < checkedState.length; i++) {
        if (updatedCheckedState[i]) {
          choices.push(scanOption[i].toLowerCase());
        }
      }

      return { ...prev, options: choices };
    });
  };

  const handleRefresh = () => {
    window.location.reload();
  };

  return (
    <div className="app-container">
      <div className="main-content">
        <header className="App-header">
          <div className="header-content">
            <img 
              src="/sss_logo.png" 
              className="header-logo" 
              alt="logo" 
              onClick={handleRefresh}
              style={{ cursor: 'pointer' }}
            />
            <h1 className="App-title">SUSSANAH</h1>
          </div>
        </header>

        <div className="App-info">
          <InfoCard
            title="Sentiment Analysis"
            children={"Sussannah analyzes the underlying sentiment, and provides an assessment based on the emotional tone of the text."}
          />

          <InfoCard
            title="Spam Detection"
            children={"Sussanah analyzes the emotion in the text and displays a pie chart of emotions shown."}
          />

          <InfoCard
            title="Summarize"
            children={"Sussanah condenses the text into a brief overview capturing the main points."}
          />
        </div>

        <div className="App-description">
          <form onSubmit={getData}>
            <textarea
              ref={textareaRef}
              className="text-input"
              type="text"
              name="paragraph"
              value={analysisForm.paragraph}
              onChange={(e) => onChangeHandler(e.target)}
              placeholder="Start your first message with Sussanah"
            />
          </form>
        </div>

        <form className="form" onSubmit={getData}>
          <div className="options-container">
            {scanOption.map((name, index) => {
              return (
                <div className="option-item" key={index}>
                  <input
                    type="checkbox"
                    id={`custom-checkbox-${index}`}
                    name={name}
                    value={name}
                    checked={checkedState[index]}
                    onChange={() => handleOnChange(index)}
                    className="checkbox-input"
                  />
                  <label
                    htmlFor={`custom-checkbox-${index}`}
                    className="checkbox-label"
                  >
                    {name}
                  </label>
                </div>
              );
            })}
          </div>
          
          <div className="submit-container">
            <button className="submit-button" type="submit">
              Analyze Text
            </button>
          </div>
        </form>

        {result && (
          <div className="results-section">
            <h2>Analysis Results</h2>
            <div className="Results-container">
              <div className="Charts-container">
                {(result.options.spam != null || result.options.sentiment != null) && (
                  <p className="result-text">Result: {result.options}</p>
                )}
                {spamData && (
                  <div className="chart-card">
                    <h3>Spam Analysis</h3>
                    <PieChart chartData={spamData} options={chartOptions} />
                  </div>
                )}
                {sentimentData && (
                  <div className="chart-card">
                    <h3>Sentiment Analysis</h3>
                    <PieChart chartData={sentimentData} options={chartOptions} />
                  </div>
                )}
              </div>
              {result.paragraph && (
                <div className="summary-card">
                  <h3>Summary</h3>
                  <p className="summary-text">{result.paragraph}</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;