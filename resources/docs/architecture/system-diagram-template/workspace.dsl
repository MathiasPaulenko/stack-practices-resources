// Structurizr DSL — generates C4 views from a single source of truth
// Serve locally: docker run -it --rm -p 8080:8080 -v $PWD:/usr/local/structurizr structurizr/lite

workspace {

    model {
        customer = person "Customer" "Checks balance and makes transfers."
        agent = person "Support Agent" "Handles customer tickets."

        email = softwareSystem "Email System" "External notification delivery." "External"
        kyc = softwareSystem "KYC Provider" "Identity verification." "External"
        mainframe = softwareSystem "Mainframe Core" "Legacy account data." "External"

        bank = softwareSystem "Online Banking System" {
            web = container "Web App" "React SPA" "React"
            mobile = container "Mobile App" "React Native" "React Native"
            api = container "API Application" "REST API" "Node.js, Express"
            worker = container "Notification Worker" "Queue consumer" "Node.js"
            db = container "PostgreSQL" "Primary store" "Database"
            cache = container "Redis" "Session cache" "Database"
            queue = container "RabbitMQ" "Message broker" "Message Queue"
        }

        customer -> web "Uses"
        customer -> mobile "Uses"
        agent -> web "Manages tickets"
        web -> api "REST / JSON"
        mobile -> api "REST / JSON"
        api -> db "Reads/writes"
        api -> cache "Reads/writes"
        api -> queue "Enqueues"
        queue -> worker "Delivers"
        worker -> email "SMTP"
        api -> kyc "Verifies identity"
        api -> mainframe "Account data"
    }

    views {
        systemContext bank {
            include *
            autolayout lr
        }
        container bank {
            include *
            autolayout lr
        }
        theme default
    }
}
