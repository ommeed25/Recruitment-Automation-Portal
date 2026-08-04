import {
    LineChart,
    Line,
    CartesianGrid,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer
} from "recharts";

const data = [
    { day: "Mon", jobs: 4 },
    { day: "Tue", jobs: 8 },
    { day: "Wed", jobs: 5 },
    { day: "Thu", jobs: 10 },
    { day: "Fri", jobs: 12 },
    { day: "Sat", jobs: 7 },
    { day: "Sun", jobs: 9 },
];

export default function WeeklyChart() {
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