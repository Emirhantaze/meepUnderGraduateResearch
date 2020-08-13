import React from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import { Navbar } from './components/Navbar';
import { SimShow } from './components/SimShow';
import { SimAddData } from './components/SimAddData';
import DataContextProvider from './DataContext';
import ViewportProvider from "./ViewPortContext";

function App() {
  return (
    <div className="App ">
    <DataContextProvider>
    <ViewportProvider>
    <Navbar/>
    <SimShow/>
    <SimAddData/> 
    </ViewportProvider>
    </DataContextProvider>
    </div>
  );
}

export default App;
