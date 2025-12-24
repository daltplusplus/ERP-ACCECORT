from src.dashboard.dashboard import DashboardDTO
from src.dashboard.dashboardRepository import DashboardRepository
from datetime import datetime


class DashboardService:

    def __init__(self, repo: DashboardRepository):
        self.repo = repo

    def summary(self, session):
        now = datetime.now()
        since = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        until = now
        self.repo.set_session(session)

        return DashboardDTO(
            average=self.repo.average_ticket(since, until),
            ticketsAmount=self.repo.tickets_amount(since, until),
            grow=self.repo.grow_vs_last_month(since, until),
            top_clients=self.repo.top_clients(since, until),
            total=self.repo.total_sales(since, until)
        )
