from fastapi import Request
from fastapi.responses import PlainTextResponse
from models import Policy, Subscription
from db import SessionLocal

def handle_ussd(request_data: dict):
    session_id = request_data.get("sessionId")
    phone_number = request_data.get("phoneNumber")
    text = request_data.get("text", "")
    parts = text.split("*") if text else []

    db = SessionLocal()

    # Language selection
    if len(parts) == 0 or parts[0] == "":
        return PlainTextResponse("CON Welcome to Crop Insurance\nKaribu kwa Bima ya Mazao\n1. English\n2. Kiswahili")

    lang = parts[0]

    if lang not in ["1", "2"]:
        return PlainTextResponse("END Invalid language option.")

    # Texts per language
    L = {
        "1": {  # English
            "main": "CON Main Menu\n1. View Policies\n2. Subscribe\n3. My Subscriptions\n4. Pay for Policy",
            "choose_policy": "CON Choose Policy to Subscribe:\n",
            "sub_success": "END Subscribed to {} successfully!",
            "invalid_policy": "END Invalid policy selected.",
            "my_subs": "END Your Subscriptions:\n{}",
            "no_subs": "END You have no subscriptions.",
            "pay_menu": "CON Choose policy to pay:\n",
            "pay_success": "END STK Push initiated for {}",
            "invalid_option": "END Invalid option.",
        },
        "2": {  # Swahili
            "main": "CON Menyu Kuu\n1. Tazama Sera\n2. Jiunge\n3. Usajili Wangu\n4. Lipa Kwa Sera",
            "choose_policy": "CON Chagua Sera ya Kujiunga:\n",
            "sub_success": "END Umejiunga na {} kwa mafanikio!",
            "invalid_policy": "END Sera sio halali.",
            "my_subs": "END Usajili Wako:\n{}",
            "no_subs": "END Huna usajili wowote.",
            "pay_menu": "CON Chagua sera ya kulipa:\n",
            "pay_success": "END STK Push imeanzishwa kwa {}",
            "invalid_option": "END Chaguo sio halali.",
        },
    }

    messages = L[lang]

    if len(parts) == 1:
        return PlainTextResponse(messages["main"])

    action = parts[1]

    # 1. View Policies
    if action == "1":
        policies = db.query(Policy).all()
        if not policies:
            return PlainTextResponse("END No policies found.")
        menu = "\n".join([f"{i+1}. {p.name} - KES {p.premium_amount}" for i, p in enumerate(policies)])
        return PlainTextResponse(f"END Available Policies:\n{menu}")

    # 2. Subscribe
    if action == "2":
        if len(parts) == 2:
            policies = db.query(Policy).all()
            menu = "\n".join([f"{i+1}. {p.name}" for i, p in enumerate(policies)])
            return PlainTextResponse(messages["choose_policy"] + menu)
        elif len(parts) == 3:
            try:
                index = int(parts[2]) - 1
                policy = db.query(Policy).offset(index).limit(1).first()
                if policy:
                    exists = db.query(Subscription).filter_by(phone_number=phone_number, policy_id=policy.id).first()
                    if exists:
                        return PlainTextResponse(f"END Already subscribed to {policy.name}.")
                    subscription = Subscription(phone_number=phone_number, policy_id=policy.id)
                    db.add(subscription)
                    db.commit()
                    return PlainTextResponse(messages["sub_success"].format(policy.name))
                else:
                    return PlainTextResponse(messages["invalid_policy"])
            except:
                return PlainTextResponse("END Error subscribing.")

    # 3. My Subscriptions
    if action == "3":
        subs = db.query(Subscription).filter_by(phone_number=phone_number).all()
        if not subs:
            return PlainTextResponse(messages["no_subs"])
        lines = []
        for sub in subs:
            policy = db.query(Policy).filter_by(id=sub.policy_id).first()
            if policy:
                lines.append(f"- {policy.name}")
        return PlainTextResponse(messages["my_subs"].format("\n".join(lines)))

    # 4. Pay for Subscription (STK simulation)
    if action == "4":
        subs = db.query(Subscription).filter_by(phone_number=phone_number).all()
        if len(parts) == 2:
            if not subs:
                return PlainTextResponse(messages["no_subs"])
            lines = [f"{i+1}. {db.query(Policy).filter_by(id=s.policy_id).first().name}" for i, s in enumerate(subs)]
            return PlainTextResponse(messages["pay_menu"] + "\n".join(lines))
        elif len(parts) == 3:
            try:
                index = int(parts[2]) - 1
                sub = subs[index]
                policy = db.query(Policy).filter_by(id=sub.policy_id).first()
                # Simulated STK Push (integrate with Safaricom Daraja here)
                # stk_push(phone_number, policy.premium_amount, policy.name)
                return PlainTextResponse(messages["pay_success"].format(policy.name))
            except:
                return PlainTextResponse(messages["invalid_policy"])

    return PlainTextResponse(messages["invalid_option"])
