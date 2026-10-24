from apps.core_users.choices import ApprovalStatus
from apps.core_users.models.workflow_model import ApprovalWorkflow

class WorkflowService:
    @staticmethod
    def initiate_workflow(user) -> ApprovalWorkflow:
        return ApprovalWorkflow.objects.create(
            user=user,
            status=ApprovalStatus.PENDING
        )

    @staticmethod
    def update_workflow_status(workflow_id: int, new_status: str, reason: str = None) -> ApprovalWorkflow:
        workflow = ApprovalWorkflow.objects.get(id=workflow_id)
        workflow.status = new_status
        if reason:
            workflow.rejection_reason = reason
        workflow.save()
        return workflow