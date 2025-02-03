import React, { useState } from "react";
import "./Styles.css";
import LanguageSelector from "./LanguageSelector";
import { Link } from "react-router-dom";

const Translate = () => {
  const [text, setText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [sourceLang, setSourceLang] = useState("en");
  const [targetLang, setTargetLang] = useState("hi");

  const handleTranslate = async () => {
    const response = await fetch("http://127.0.0.1:5000/translate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: text,
        sourceLang: sourceLang,
        targetLang: targetLang,
      }),
    });

    const data = await response.json();
    if (data.translatedText) {
      setTranslatedText(data.translatedText);
    } else {
      setTranslatedText("Error: Unable to translate.");
    }
  };

  return (
    <>
    <div>
    <h1><center>Travel Assistor</center></h1>
    <div className="translator-container">
      <h2>Text Translator</h2>
      <textarea
        placeholder="Enter text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        className="text-area"
      />
      <div className="dropdown-container">
        <LanguageSelector
          selectedLang={sourceLang}
          onChange={setSourceLang}
        />
        <LanguageSelector
          selectedLang={targetLang}
          onChange={setTargetLang}
        />
      </div>
      <button onClick={handleTranslate} className="translate-button">
        Translate Text
      </button>
      <textarea
        placeholder="Translation"
        value={translatedText}
        readOnly
        className="text-area"
      />
    </div>
    <Link to="/audio-translation">Go to Audio Translation</Link>
    </div>
    </>
  );
  
};

export default Translate;





