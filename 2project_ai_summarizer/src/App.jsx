import Hero from "./components/Hero";
import Demo from "./components/Demo";

import {
  BrowserRouter as Router,
  Routes,
  Route,
  useRoutes,
  NavLink,
} from "react-router-dom";

import "./App.css";
import AiSummarizer from "./components/AiSummarizer";
import AiWritingAssistant from "./components/AiWritingAssistant";
import Test from "./components/Test";
import Home from "./components/Home";

const App = () => {
  // <Test />
  // let routes = useRoutes([
  //   { path: "summarize", element: <AiSummarizer /> },
  //   { path: "write", element: <AiWritingAssistant /> },
  //   { path: "/", element: <Test /> },
  //   // ...
  // ]);
  // return routes;

  //    <Routes>
  //   <Route path="/" exact element={<AiSummarizer />} />
  //   <Route path="/demo" element={<Demo />} />
  //   {/* <Route path="*" element={<Hero />} /> */}
  // </Routes> 
  return (
    <>
      <AiSummarizer />
    </>
  )
};

// const AppWrapper = () => {
//   return (
//     <Router>
//       <App />
//     </Router>
//   );
// };

export default App;
