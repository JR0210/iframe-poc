import { useRef, useEffect, useCallback } from "react";
import logo from "./logo.svg";
import "./App.css";

function App() {
  const iframeRef = useRef();

  useEffect(() => {
    iframeRef.current.contentWindow.postMessage(
      {
        type: "SET_IFRAME_HEIGHT",
        height: "500px",
      },
      "*"
    );
  }, [iframeRef]);

  function handleMouseMove(e) {
    console.log(e);
  }

  const iframeCallbackRef = useCallback(
    (node) => (iframeRef.current = node),
    []
  );

  useEffect(() => {
    const onBlur = (e) => {
      if (
        document.activeElement &&
        document.activeElement.nodeName.toLowerCase() === "iframe" &&
        iframeRef.current &&
        iframeRef.current === document.activeElement
      ) {
        console.log(e, "blur");
        // infer a click event
        console.log(iframeRef.current);
      }
    };

    window.addEventListener("blur", onBlur);

    return () => {
      window.removeEventListener("blur", onBlur);
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <iframe
        src="https://dreamcargiveaways.co.uk/current-competitions/"
        title="preview"
        frameborder="0"
        style={{ height: "600px", width: "600px" }}
        ref={iframeCallbackRef}
      ></iframe>
    </div>
  );
}

export default App;
