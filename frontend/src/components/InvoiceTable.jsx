import React from "react";

export default function InvoiceTable({invoices}){
  return (
    <div>
      <h2>Invoices</h2>
      <table style={{width:"100%", borderCollapse:"collapse"}}>
        <thead>
          <tr style={{textAlign:"left"}}>
            <th>Inv No</th><th>Date</th><th>Airline</th><th>Amount</th><th>GSTIN</th><th>File</th>
          </tr>
        </thead>
        <tbody>
          {invoices.map(i=>(
            <tr key={i.id}>
              <td style={{padding:6}}>{i.invoice_number}</td>
              <td style={{padding:6}}>{i.invoice_date}</td>
              <td style={{padding:6}}>{i.airline}</td>
              <td style={{padding:6}}>{i.amount}</td>
              <td style={{padding:6}}>{i.gstin}</td>
              <td style={{padding:6}}>
                {i.file_name ? <a href={`/api/download-file/${i.ticket}`} target="_blank" rel="noreferrer">Open PDF</a> : "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
