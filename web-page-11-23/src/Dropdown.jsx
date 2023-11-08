/**
 * this item is consist for making the dropdown and placing the items in it
 */
import { v4 as uuidv4 } from 'uuid';
import Dropdown from 'react-bootstrap/Dropdown';
import { Selectioncontext, selectGoldRatio, selectSilverRatio } from "./Selectionconcext";
import { useContext } from "react";

const DropdownUs = ({ title, names, selection_id }) => {
    const { selection, selectionSetter } = useContext(Selectioncontext)
    function clickevent(data, id) {
        console.log(data, id)
        if (id === "pdms") {
            selectionSetter({
                ...selection,
                isPDMSRatioSelected: true,
                PDMSRatio: data,
                SilverRatios: selectSilverRatio(window.data, data),
                GoldRatios: selectGoldRatio(window.data, data),
                GoldRatio: null,
                SilverRatio: null,
            })
        }
        else if (id === "gold") {
            selectionSetter({
                ...selection,
                isPDMSRatioSelected: true,
                GoldRatio: data,
                SilverRatio: 100 - data - selection["PDMSRatio"]
            })
        }
        else if (id === "silver") {
            selectionSetter({
                ...selection,
                isPDMSRatioSelected: true,
                SilverRatio: data,
                GoldRatio: 100 - data - selection["PDMSRatio"]
            })
        }
        else if (id === "polarization") {
            selectionSetter({
                ...selection,
                Polarization: data
            })
        }
        else if (id === "spacing") {
            selectionSetter({
                ...selection,
                Spacing: data
            })
        }
        else if (id === "type") {
            selectionSetter({
                ...selection,
                type: data
            })
        }
    }
    return (<div className='col'>

        <Dropdown >
            <Dropdown.Toggle variant="info" id="dropdown-basic">
                {title}
            </Dropdown.Toggle>
            {

                (names != null) && (<Dropdown.Menu>
                    {names.map(x => <Dropdown.Item key={uuidv4()}><div onClick={() => { clickevent(x, selection_id) }}>{x}</div></Dropdown.Item>)}
                </Dropdown.Menu>
                )}
        </Dropdown>
    </div>
    );
};


export default DropdownUs;


