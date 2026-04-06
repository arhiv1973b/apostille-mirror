/**
 * CASE-MACHERET Data Integration Module
 * Source: apostille_registry_working_5.signed.pdf
 */
const apostilleData = [
    { id: "1", code: "IMWM44AZGX6N6", case: "2013073817848", dateIssue: "04.01.2021", dateApostille: "18.01.2021", series: "000278", signedBy: "Топорец Ирина", position: "Подписант", department: "Минюст" },
    { id: "2", code: "BOUS9XAQDTFH2", case: "2013073851064", dateIssue: "11.02.2021", dateApostille: "24.02.2021", series: "07-6/3-41", signedBy: "Мирон Алёна", position: "И.О. Вицепрезидента суда", department: "Судебная власть" },
    { id: "3", code: "CQ0VC27VGTCK6", case: "2013073880545", dateIssue: "24.03.2021", dateApostille: "29.03.2021", series: "21-021527", signedBy: "Гонза Наталья", position: "Подписант", department: "Минюст" },
    { id: "4", code: "DR4Y1584JW9F4", case: "2013073886585", dateIssue: "12.11.2003", dateApostille: "05.04.2021", series: "1-649/2003", signedBy: "Мирон Алёна", position: "И.Ο. вицепрезидента", department: "Судебная власть" },
    { id: "5", code: "7H2Q3790FZEI5", case: "2013073926618", dateIssue: "13.10.1998", dateApostille: "18.05.2021", series: "1-568/98", signedBy: "Мирон Алёна", position: "И.О. Вицепрезидента", department: "Судебная власть" },
    { id: "97", code: "EOYXD0FZ7Y8P2", case: "2013074031106", dateIssue: "13.08.2021", dateApostille: "13.08.2021", series: "N/A", signedBy: "Vinogradov Mihail", position: "Подписант", department: "Минюст" }
];

function renderApostilleTable() {
    const tableBody = document.querySelector('#apostille-table tbody');
    if (!tableBody) return;
    tableBody.innerHTML = apostilleData.map(item => `
        <tr>
            <td>${item.id}</td>
            <td style="font-family: monospace; color: #00ff41;">${item.code}</td>
            <td>${item.dateIssue}</td>
            <td>${item.dateApostille}</td>
            <td>${item.series}</td>
            <td>${item.signedBy}</td>
            <td>${item.position}</td>
            <td>${item.department}</td>
            <td><a href="https://github.com/arhiv1973b/apostille-legal-case/blob/main/docs/${item.code}.pdf" target="_blank">Download</a></td>
        </tr>`).join('');
}
document.addEventListener('DOMContentLoaded', renderApostilleTable);
