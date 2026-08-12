import {
    LineChart,
    Line,
    CartesianGrid,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer
} from "recharts";
import { useEffect, useState } from "react";

export default function WeeklyChart() {
    const [data, setData] = useState([
        { day: "Mon", jobs: 0 },
        { day: "Tue", jobs: 0 },
        { day: "Wed", jobs: 0 },
        { day: "Thu", jobs: 0 },
        { day: "Fri", jobs: 0 },
        { day: "Sat", jobs: 0 },
        { day: "Sun", jobs: 0 },
    ]);

    useEffect(() => {
        const loadWeeklyData = async () => {
            try {
                const { getWeeklyJobStats } = await import("../../services/dashboard");
               const weeklyData = await getWeeklyJobStats();

                console.log("WEEKLY DATA:", weeklyData);
                console.log("IS ARRAY:", Array.isArray(weeklyData));

                setData(weeklyData);
            } catch (error) {
                console.error("Failed to load weekly stats:", error);
            }
        };

        void loadWeeklyData();
    }, []);

    return (
        <ResponsiveContainer width="100%" height={320}>
            <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Line
                    type="monotone"
                    dataKey="jobs"
                    stroke="#2563eb"
                    strokeWidth={3}
                />
            </LineChart>
        </ResponsiveContainer>
    );
}