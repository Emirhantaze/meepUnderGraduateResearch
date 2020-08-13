import React from 'react'
import { useState } from 'react'
import { createContext } from 'react'


export const DataContext = createContext()


export default function DataContextProvider(props) {
    const [data,dataSetter] = useState([])
    return (
        <div>
            <DataContext.Provider value={
                {data:data,dataSetter:dataSetter}
            }>{props.children}</DataContext.Provider> 
        </div>
    )
}
