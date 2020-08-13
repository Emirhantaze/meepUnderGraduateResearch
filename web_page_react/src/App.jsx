import React from 'react';
import 'bootstrap/dist/css/bootstrap.css';
import { Navbar } from './components/Navbar';
import { SimShow } from './components/SimShow';
import { SimAddData } from './components/SimAddData';
import DataContextProvider from './DataContext';


function App() {
  return (
    <div className="App">
    <DataContextProvider>
      
    <Navbar/>
    <SimShow/>
    <SimAddData/> 
    
    </DataContextProvider>
    </div>
  );
}

export default App;
