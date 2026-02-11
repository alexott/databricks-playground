output "vm_public_ip" {
  value       = aws_instance.vm.public_ip
  description = "Public IP address of the VM"
}

output "vm_public_dns" {
  value       = aws_instance.vm.public_dns
  description = "Public DNS name of the VM"
}

output "vm_private_ip" {
  value       = aws_instance.vm.private_ip
  description = "Private IP address of the VM"
}

output "iam_role_arn" {
  value = aws_iam_role.assume_role.arn
  description = "ARN IAM role that will be used as subject"
}
