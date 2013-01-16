Bitdeli Badge for GitHub
------------------------

Raw request logs from all `Bitdeli badges <https://bitdeli.com/docs/badge.html>`_ under a GitHub account.

Create a badge at https://bitdeli.com/free.

- **Source:** GitHub page loads.

- **Historical data:** All historical data since the badge was added.

- **Retention:** 90 days.

- **Schema:**
    .. code-block:: python

    {
        "repos": {
            "repository-name": [
                {
                    "ip": ip address of the client,
                    "user-agent": user agent of the client,
                    "referrer": repository name,
                    "tstamp": timestamp
                }
                ...
            ]
            ...
        }
    }

- **Update interval:** 1 hour

- **Code:** `bitdeli/profile-ghbadge <https://github.com/bitdeli/profile-ghbadge>`_

