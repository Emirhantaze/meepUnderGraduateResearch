export const divide = (arr1,arr2)=>{
    let out= []
    for(let i = 0 ; i< arr1.length;i++){
        out.push((arr1[i]/arr2[i]))
    }
    return out
}

export const square = (arr1)=>{
    let out= []
    for(let i = 0 ; i< arr1.length;i++){
        out.push((arr1[i]*arr1[i]))
    }
    return out
}
