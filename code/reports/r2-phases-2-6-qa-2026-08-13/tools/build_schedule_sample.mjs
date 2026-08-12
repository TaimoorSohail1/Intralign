import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputDir = "C:/Users/Hp/Documents/ChatGPT/oslo-knowledge/code/outputs/r2-live-data";
await fs.mkdir(outputDir, { recursive: true });

const workbook = Workbook.create();
const schedule = workbook.worksheets.add("Schedule");
schedule.getRange("A1:G1").merge();
schedule.getRange("A1").values = [["DevNorth 2026 — Delivery Schedule & Resourcing"]];
schedule.getRange("A1:G1").format = {
  fill: "#193047",
  font: { bold: true, color: "#FFFFFF", size: 16 },
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
schedule.getRange("A2:G2").values = [["Workstream", "Owner", "Start", "Due", "Status", "Budget PKR", "Evidence"]];
schedule.getRange("A2:G2").format = { fill: "#E7EEF5", font: { bold: true, color: "#193047" } };
schedule.getRange("A3:G7").values = [
  ["Venue & network", "Aisha Khan", new Date("2026-08-20"), new Date("2026-09-05"), "On track", 4200000, "500-device failover test"],
  ["Registration", "Omar Siddiqui", new Date("2026-08-15"), new Date("2026-09-11"), "On track", 1800000, "405 confirmed attendees"],
  ["Programme", "Sara Ali", new Date("2026-08-12"), new Date("2026-09-09"), "At risk", 6500000, "18 speakers + backup keynote"],
  ["Sponsors", "Bilal Ahmed", new Date("2026-08-10"), new Date("2026-09-12"), "On track", 2800000, "PKR 12m contracted"],
  ["Event operations", "Hina Raza", new Date("2026-09-01"), new Date("2026-09-18"), "Not started", 8700000, "Run-of-show rehearsal"],
];
schedule.getRange("C3:D7").format.numberFormat = "dd mmm yyyy";
schedule.getRange("F3:F7").format.numberFormat = "#,##0";
schedule.getRange("A8:E8").merge();
schedule.getRange("A8").values = [["Total delivery budget"]];
schedule.getRange("F8").formulas = [["=SUM(F3:F7)"]];
schedule.getRange("A8:G8").format = { fill: "#F4F7FA", font: { bold: true, color: "#193047" } };
schedule.getRange("F8").format.numberFormat = "#,##0";
schedule.freezePanes.freezeRows(2);
schedule.getRange("A1:G8").format.wrapText = true;
schedule.getRange("A1:G8").format.autofitColumns();
schedule.getRange("A1:G8").format.autofitRows();
schedule.getRange("A:A").format.columnWidth = 22;
schedule.getRange("G:G").format.columnWidth = 31;

const preview = await workbook.render({ sheetName: "Schedule", range: "A1:G8", autoCrop: "all", scale: 1.25, format: "png" });
await fs.writeFile(`${outputDir}/devnorth-2026-schedule-preview.png`, new Uint8Array(await preview.arrayBuffer()));
const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(`${outputDir}/devnorth-2026-schedule.xlsx`);
console.log(`${outputDir}/devnorth-2026-schedule.xlsx`);
