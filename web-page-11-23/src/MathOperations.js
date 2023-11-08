import { propTypes } from "react-bootstrap/esm/Image"

export const divide = (arr1, arr2) => {
    let out = []
    for (let i = 0; i < arr1.length; i++) {
        out.push((arr1[i] / arr2[i]))
    }
    return out
}

export const square = (arr1) => {
    let out = []
    for (let i = 0; i < arr1.length; i++) {
        out.push((arr1[i] * arr1[i]))
    }
    return out
}

export const reduceDimention = (arr) => {
    return arr.map((val) => { return val[0] })
}

export const minussign = (arr) => {
    return arr.map((val) => { return -val })
}

export const abso = (arr) => {
    return arr.map((val) => { return val < 0 ? -val : val })
}

export const addition = (arr,arr1) => {
    var arr2 =  [...arr]
    for (let i = 0; i< arr.length;i++)
    {
        arr2[i] =arr[i] + arr1[i]; 
    }
    return arr2;
    
}

