import React from "react";

export default function PassengerTable({passengers, onDownload, onParse})
{ console.log(passengers)
  return (
    <div style={{marginTop:10}}>
      <h2>Passengers</h2>
      <table style={{width:"100%", borderCollapse:"collapse"}}>
        <thead>
          <tr style={{textAlign:"left"}}>
            <th>Ticket</th><th>Name</th><th>Download</th><th>Parse</th><th>Status</th>
          </tr>
        </thead>
        <tbody>
          {/* {passengers.map(p=>(
            <tr key={p.ticket}>
              <td style={{padding:6}}>{p.ticket}</td>
              <td style={{padding:6}}>{p.name}</td>
              <td style={{padding:6}}>
                <button onClick={()=>onDownload(p.Ticket)}>Download</button>
              </td>
              <td style={{padding:6}}>
                <button onClick={()=>onParse(p.Ticket)} disabled={p.download_status!=="Success"}>Parse</button>
              </td>
              <td style={{padding:6}}>
                <strong>Download:</strong> {p.download_status} <br/>
                <strong>Parse:</strong> {p.parse_status}
              </td>
            </tr>
          ))} */}


          {passengers.map(passenger => (
  <tr key={passenger.ticket}>
    <td>{passenger.ticket}</td>
    <td>{passenger.name}</td>
    <td>
      <button onClick={() => onDownload(passenger.ticket)}>Download</button>
      <button onClick={() => onParse(passenger.ticket)}>Parse</button>
    </td>
    <td>Download: {passenger.download_status}</td>
    <td>Parse: {passenger.parse_status}</td>
  </tr>
))}
        </tbody>
      </table>
    </div>
  )
}
