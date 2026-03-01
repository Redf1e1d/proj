import { useEffect, useState } from "react";
import API from "../api/api";

export default function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    API.get("/developers")
      .then((res) => setData(res.data))
      .catch(() => alert("Unauthorized"));
  }, []);

  return (
    <div>
      <h2>Developers</h2>
      {data.map((d) => (
        <div key={d.id}>{d.name}</div>
      ))}
    </div>
  );
}