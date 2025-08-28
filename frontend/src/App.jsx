import React, {useEffect, useState} from "react";
import PassengerTable from "./components/PassengerTable";
import InvoiceTable from "./components/InvoiceTable";

export default function App(){
  const [passengers, setPassengers] = useState([]);
  const [invoices, setInvoices] = useState([]);
  const [summary, setSummary] = useState([]);
  const [threshold, setThreshold] = useState(5000);

  async function loadPassengers(){
    const r = await fetch("http://127.0.0.1:8000/api/passengers");
    console.log(r)
    setPassengers(await r.json());
  }
  async function loadInvoices(){
    const r = await fetch("http://127.0.0.1:8000/api/invoices");
    setInvoices(await r.json());
  }
  async function loadSummary(){
    const r = await fetch("http://127.0.0.1:8000/api/summary");
    setSummary(await r.json());
  }

  useEffect(()=>{
    loadPassengers(); loadInvoices(); loadSummary();
  }, []);

  async function onDownload(ticket){
    await fetch(`http://127.0.0.1:8000/api/download/${ticket}`, {method:"POST"});
    await loadPassengers();
    await loadInvoices();
  }
  async function onParse(ticket){
    await fetch(`http://127.0.0.1:8000/api/parse/${ticket}`, {method:"POST"});
    await loadPassengers();
    await loadInvoices();
  }
  async function showHighValue(){
    const r = await fetch(`http://127.0.0.1:8000/api/high-value/${threshold}`);
    const data = await r.json();
    alert(`Found ${data.length} invoices above ${threshold}. Check console.`);
    console.log(data);
  }

  return (
    <div style={{padding:20,fontFamily:"Arial"}}>
      <h1>Invoice Dashboard (Demo)</h1>
      <PassengerTable passengers={passengers} onDownload={onDownload} onParse={onParse}/>
      <div style={{marginTop:20}}>
        <InvoiceTable invoices={invoices}/>
      </div>
      <div style={{marginTop:20}}>
        <h3>Summary</h3>
        <pre>{JSON.stringify(summary, null, 2)}</pre>
        <div>
          <input type="number" value={threshold} onChange={e=>setThreshold(e.target.value)}/>
          <button onClick={showHighValue}>Show High Value</button>
        </div>
      </div>
    </div>
  )
}
