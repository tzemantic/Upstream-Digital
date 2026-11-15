// Auto-reply to website contact form submissions.
//
// Netlify runs a function named "submission-created" automatically after every
// verified (non-spam) Netlify Forms submission. This one emails the visitor a short
// thank-you through Resend (https://resend.com).
//
// Settings (Netlify > Project configuration > Environment variables):
//   RESEND_API_KEY  required. A Resend API key with "Sending access" only.
//   AUTOREPLY_FROM  optional. Defaults to "Upstream Digital <hello@getupstreamdigital.com>".
//   AUTOREPLY_REPLY_TO optional. Defaults to "tyler@getupstreamdigital.com".
//
// Kept deliberately plain (no links, nothing echoed from the visitor except a short
// first name) so nobody can use the form to send useful content to a stranger.

const FROM_DEFAULT = "Upstream Digital <hello@getupstreamdigital.com>";
const REPLY_TO_DEFAULT = "tyler@getupstreamdigital.com";
const PHONE = "+1 (860) 450-6983";

// A short, safe first name for the greeting, or "" if it doesn't look like a name.
function greetingName(raw) {
  if (typeof raw !== "string") return "";
  const first = raw.trim().split(/\s+/)[0] || "";
  // Letters (any language), apostrophes, hyphens and periods only; no links or symbols.
  if (!/^[\p{L}][\p{L}'’.-]{0,29}$/u.test(first)) return "";
  return first.charAt(0).toUpperCase() + first.slice(1);
}

function validEmail(raw) {
  return typeof raw === "string" && raw.length <= 254 && /^[^\s@<>()",;:]+@[^\s@<>()",;:]+\.[a-z]{2,}$/i.test(raw.trim());
}

function buildEmail(name) {
  const hi = name ? `Hi ${name}, thanks for reaching out!` : "Hi there, thanks for reaching out!";
  const text = [
    hi,
    "",
    "We've received your message and will be in touch as soon as possible.",
    "",
    `If it's time-sensitive, you're welcome to give us a call at ${PHONE}.`,
    "",
    "Talk soon,",
    "The Upstream Digital team",
  ].join("\n");
  const html = brandedHtml(name);
  return { subject: "Thanks for reaching out to Upstream Digital", text, html };
}

// Branded HTML version, matching the website: abyss header with the logo, a brand-blue
// "current" line, foam background, Montserrat where the mail app supports web fonts.
// Table layout and inline styles so it renders in Outlook, Gmail and Apple Mail.
function brandedHtml(name) {
  const ABYSS = "#070D1C", NAVY = "#1D2F4F", BRAND = "#6D94FF", SKY = "#99B9FF", FOAM = "#EEF3FF", MUTED = "#4A5D82";
  // Same font stacks as the website (--display / --body). Mail apps that can't load web fonts fall back to these.
  const FONT = "Montserrat,'Helvetica Neue',Arial,sans-serif";
  const LOGO = "https://www.getupstreamdigital.com/assets/email-logo.png";
  // Non-breaking space keeps "reaching out!" together when the headline wraps
  const headline = (name ? `Hi ${name}, thanks for` : "Hi there, thanks for") + " reaching&nbsp;out!";
  const preheader = "We've received your message and will be in touch as soon as possible.";
  return `<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light only"><meta name="supported-color-schemes" content="light only">
<title>Thanks for reaching out to Upstream Digital</title>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  body{margin:0;padding:0;background:${FOAM}}
  a{color:${BRAND}}
  @media (max-width:620px){
    .card{width:100%!important;border-radius:0!important}
    .pad{padding-left:24px!important;padding-right:24px!important}
    .h1{font-size:26px!important}
  }
</style>
</head>
<body style="margin:0;padding:0;background:${FOAM}">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:${FOAM}">${preheader}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:${FOAM}">
<tr><td align="center" style="padding:32px 12px">
  <table role="presentation" class="card" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#ffffff;border-radius:20px;overflow:hidden">
    <tr><td class="pad" bgcolor="${ABYSS}" style="background:${ABYSS};padding:28px 40px 26px">
      <img src="${LOGO}" width="180" height="26" alt="Upstream Digital" style="display:block;border:0;width:180px;height:auto;color:#ffffff;font:700 20px ${FONT}">
    </td></tr>
    <tr><td bgcolor="${BRAND}" style="height:4px;line-height:4px;font-size:0;background:${BRAND};background-image:linear-gradient(90deg,${NAVY},${BRAND} 55%,${SKY})">&nbsp;</td></tr>
    <tr><td class="pad" bgcolor="${ABYSS}" style="background:${ABYSS};padding:36px 40px 40px">
      <p style="margin:0 0 16px;font:700 13px/1.2 ${FONT};letter-spacing:.14em;text-transform:uppercase;color:${SKY}"><span style="display:inline-block;width:28px;height:2px;margin:0 12px 0 0;vertical-align:middle;background:${BRAND};border-radius:2px"></span>Message received</p>
      <h1 class="h1" style="margin:0 0 14px;font:700 32px/1.1 ${FONT};letter-spacing:-.025em;color:#ffffff">${headline}</h1>
      <p style="margin:0;font:400 17px/1.6 ${FONT};color:${FOAM}">We've received your message and will be in touch as soon as possible.</p>
    </td></tr>
    <tr><td class="pad" style="padding:36px 40px 12px">
      <p style="margin:0 0 20px;font:400 17px/1.6 ${FONT};color:${NAVY}">If it's time-sensitive, you're welcome to give us a call.</p>
      <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
        <td bgcolor="${BRAND}" style="border-radius:300px;background:${BRAND}">
          <a href="tel:+18604506983" style="display:inline-block;padding:14px 28px;font:600 16px/1 ${FONT};color:${ABYSS};text-decoration:none;border-radius:300px;white-space:nowrap">Call ${PHONE}</a>
        </td>
      </tr></table>
    </td></tr>
    <tr><td class="pad" style="padding:28px 40px 40px">
      <p style="margin:0;font:400 17px/1.6 ${FONT};color:${NAVY}">Talk soon,<br><strong style="font-weight:700">The Upstream Digital team</strong></p>
    </td></tr>
    <tr><td class="pad" bgcolor="${ABYSS}" style="background:${ABYSS};padding:24px 40px">
      <p style="margin:0 0 6px;font:600 14px/1.5 ${FONT};color:#ffffff">Upstream Digital <span style="color:${SKY};font-weight:400">&nbsp;Greenwich, CT</span></p>
      <p style="margin:0;font:400 13px/1.5 ${FONT};color:${SKY}"><a href="https://www.getupstreamdigital.com" style="color:${SKY};text-decoration:underline">getupstreamdigital.com</a></p>
    </td></tr>
  </table>
  <p style="margin:18px 0 0;font:400 12px/1.5 ${FONT};color:${MUTED}">You're receiving this because you contacted us through our website.</p>
</td></tr>
</table>
</body></html>`;
}

async function handler(event) {
  let payload;
  try {
    payload = JSON.parse(event.body || "{}").payload || {};
  } catch {
    return { statusCode: 400, body: "Bad payload" };
  }
  const data = payload.data || {};
  const formName = payload.form_name || data["form-name"];
  if (formName !== "contact") return { statusCode: 200, body: "Not the contact form" };
  if (data["bot-field"]) return { statusCode: 200, body: "Skipped" };

  const to = (data.email || "").trim();
  if (!validEmail(to)) return { statusCode: 200, body: "No valid email" };

  const key = process.env.RESEND_API_KEY;
  if (!key) {
    console.error("RESEND_API_KEY is not set; auto-reply not sent.");
    return { statusCode: 200, body: "Not configured" };
  }

  const msg = buildEmail(greetingName(data.name));
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: process.env.AUTOREPLY_FROM || FROM_DEFAULT,
      to: [to],
      reply_to: process.env.AUTOREPLY_REPLY_TO || REPLY_TO_DEFAULT,
      subject: msg.subject,
      text: msg.text,
      html: msg.html,
    }),
  });
  if (!res.ok) {
    console.error("Resend error", res.status, await res.text());
    // Still 200: the submission itself is saved and emailed to us either way.
    return { statusCode: 200, body: "Auto-reply failed" };
  }
  return { statusCode: 200, body: "Auto-reply sent" };
}

module.exports = { handler, greetingName, validEmail, buildEmail, brandedHtml };
