# How the bot works
```mermaid
sequenceDiagram
    actor User
    participant T as Telegram
    participant B as Bot

    User ->> T: join
    T ->> +B: new_member_joined()
    critical Delete newcomer's messages
        B ->> +T: get_messages(new_member)
        T -->> -B: [message_id]
        B ->> T: delete_messages([message_id])
    end
    critical Silence the newcomer
        B ->> -T: restict_user(user, period)
    option after the period is through
        T ->> T: unblock(new_member)
    end
```
As a result, the newcomer can't send new messages for a specified period of time. Although he can read and sees the pinned button "Newcomer? Here!"


# Calculate karma every night
```mermaid
sequenceDiagram
    loop every night
        participant T as Telegram
        participant KK as KarmaKeeper
        participant DB as Database
        actor U as User

        KK ->> T: get_messages()
        T -->> KK: [message]
        KK ->> DB: add_reaction_counts([message.reactions])
        KK ->> DB: get_karma_shifts(threshold)
        DB -->> KK: [user, shift]
        KK ->> U: Congratulations or Warning
    end
```
