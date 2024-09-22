# DisSafe Shield API Documentation

## Description

DisSafe API is a security system designed to protect communication and the exchange of moderation information between Discord servers. With a focus on ensuring secure and efficient integration, this protocol enables global server connections, ensuring that critical data is transmitted safely and reliably

## Authentication

This API uses token-based authentication (Bearer Token). You must include the token in the `Authorisation` header in all requests.

**Exemplo**:

``` http
Authorization: Bearer <Token Here>
```

## Endpoints

### 1. Make a report

**Método**: `POST`  
**URL**: `/api/v1/report`

**Parameters:

| Parameter   | Type   | Mandatory   | Description                |
|-------------|--------|-------------|----------------------------|
| None        | None   | None        |                            |

**Exemplo de Requisição**:

```bash
curl -X POST "https://api.ip.com/api/v1/report" \
     -H "Authorization: Bearer <TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{
            "staff_username": "", # Name of the staff making the report
            "staff_id": 123456789, # ID of the staff making the report
            "banned_user": "", # Name of offending member
            "banned_user_id": 123456789, # ID of offending member
            "reason": "", # Reason for the report 
            "server_id": 123456789, # ID of the server where the report was made
            "bot": false, # Indicate whether the reported person is a bot or not
            "proof": "" # links to the report's proofs
        }'
```

**Example Answer**:

```json
{
    "message": "Report submitted successfully"
}
```

or

```json
{
    "message": "Report submitted successfully, but some URLs were invalid",
    "success": [],
    "success_but": [],
    "fails": [],
    "invalid": []
}
```

**Response Codes**:

| Code   | Description                                               |
|--------|---------------------------------------------------------|
| 500    | Failed to connect to database                           |
| 500    | Failed to insert report                                 |
| 422    | Report submitted sucessfuly, but some URLs were invalid |
| 401    | Token not provided or invalid                           |
| 400    | This route does not accept parameters                   |
| 400    | Missing required fields                                 |
| 400    | Reason not valid                                        |
| 400    | Bot not valid                                           |
| 400    | You cannot report yourself                              |
| 200    | Report submitted successfuly                            |

---

## Usage Limitations

- Limit of 1000 requests per day.

---

## Version

This API is currently in version `v1`.

---

## Contact

For more information or support, please send an e-mail to: `suporte@exemplo.com`.
