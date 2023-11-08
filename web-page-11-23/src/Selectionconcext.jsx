/**
 * bu kod sayfası seçim yapılan her türlü bilbinin saklanmasını sağlar
 * 
 * Gold oranları başlangıştan sabit olup diğer oranlar ancak gold seçildikten sonra seçilebilir olmaktadır
 * 
 * TODO diğer değişkenlerde eklenecek
 */
import React from 'react'
import { useState } from 'react'
import { createContext } from 'react'
import d from "./sample.json"

export const Selectioncontext = createContext()

export const typenames = ["Transmission", "Reflection", "Transmission Polarization Ratio", "Reflection Polarization Ratio"]

export default function SelectioncontextProvider(props) {
    const [selection, selectionSetter] = useState({
        PDMSRatios: selectPDMSRatio(d),
        PDMSRatio: null,
        isPDMSRatioSelected: false,

        GoldRatios: null,
        GoldRatio: null,
        isGoldRatioSelected: false,

        SilverRatios: null,
        SilverRatio: null,
        isSilverRatioSelected: false,

        Polarization: null,

        Spacing: null,

        type: null,
    })

    return (
        <div>
            <Selectioncontext.Provider value={
                { selection: selection, selectionSetter: selectionSetter }
            }>{props.children}</Selectioncontext.Provider>
        </div>
    )
}


// this is the peace of funtion use to delete dublicates in an array
/* https://www.shiksha.com/online-courses/articles/remove-duplicates-javascript-array/*/

export function removeDuplicates(arr) {
    return arr.filter((item,
        index) => arr.indexOf(item) === index);
}



function selectPDMSRatio(data) {
    var keys = Object.keys(data)
    keys = keys.map((key) => { return parseFloat(JSON.parse(key)["Ratio"][2]) }).sort(function (a, b) { return a - b })
    return removeDuplicates(keys)
}

export function selectSpacing(data) {
    var keys = Object.keys(data)
    keys = keys.map((key) => { return parseFloat(JSON.parse(key)["Spacing"]) }).sort(function (a, b) { return a - b })
    return removeDuplicates(keys)
}

export function selectGoldRatio(data, pdms) {
    var keys = Object.keys(data)
    keys = keys.map((key) => {
        if (parseFloat(JSON.parse(key)["Ratio"][2]) === pdms) {
            return parseFloat(JSON.parse(key)["Ratio"][0])
        }
        return null
    })
    var ret = []
    keys.forEach(elements => {
        if (elements != null && elements !== undefined && elements !== "") {
            ret.push(elements);
        }
    });
    return removeDuplicates(ret)
}

export function selectSilverRatio(data, pdms) {
    var keys = Object.keys(data)
    keys = keys.map((key) => {
        if (parseFloat(JSON.parse(key)["Ratio"][2]) === pdms) {
            return parseFloat(JSON.parse(key)["Ratio"][1])
        }
        return null
    })
    var ret = []
    keys.forEach(elements => {
        if (elements != null && elements !== undefined && elements !== "") {
            ret.push(elements);
        }
    });
    return removeDuplicates(ret)
}