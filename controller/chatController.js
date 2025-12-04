const Chat = require("../models/chat");

// simple estimator inside controller
const estimateProject = (msg) => {
  msg = msg.toLowerCase();

  if (msg.includes("gym website")) {
    return {
      time: "7-10 days",
      steps: [
        "UI/UX Design",
        "Landing Page",
        "Membership System",
        "Admin Dashboard",
        "Payment Integration"
      ]
    };
  }

  if (msg.includes("ecommerce") || msg.includes("shopping")) {
    return {
      time: "20-30 days",
      steps: [
        "Product Catalog",
        "Cart System",
        "Order Flow",
        "Admin Panel",
        "Payment Gateway"
      ]
    };
  }

  return { time: "Unknown", steps: [] };
};

exports.processChat = async (req, res) => {
  const userMessage = req.body.message;

  const estimation = estimateProject(userMessage);

  const botMessage =
    estimation.time !== "Unknown"
      ? `Estimated time: ${estimation.time}`
      : "Let me help you with that!";

  await Chat.create({
    userMessage,
    botMessage
  });

  res.json({
    reply: botMessage,
    estimation
  });
};
