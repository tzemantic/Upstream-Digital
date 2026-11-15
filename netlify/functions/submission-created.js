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
  const hi = name ? `Hi ${name},` : "Hi there,";
  const text = [
    hi,
    "",
    "Thanks for reaching out to Upstream Digital. We've received your message and will be in touch as soon as possible.",
    "",
    `If it's time-sensitive, you're welcome to call us at ${PHONE}.`,
    "",
    "Talk soon,",
    "The Upstream Digital team",
  ].join("\n");
  const html = `<!doctype html><html><body style="margin:0;padding:24px;background:#ffffff;font-family:Arial,Helvetica,sans-serif;font-size:15px;line-height:1.6;color:#1D2F4F">
<p style="margin:0 0 16px">${hi}</p>
<p style="margin:0 0 16px">Thanks for reaching out to Upstream Digital. We've received your message and will be in touch as soon as possible.</p>
<p style="margin:0 0 16px">If it's time-sensitive, you're welcome to call us at ${PHONE}.</p>
<p style="margin:0">Talk soon,<br>The Upstream Digital team</p>
</body></html>`;
  return { subject: "Thanks for reaching out to Upstream Digital", text, html };
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

module.exports = { handler, greetingName, validEmail, buildEmail };
