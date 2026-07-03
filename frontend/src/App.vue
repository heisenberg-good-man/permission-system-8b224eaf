<template>
  <div class="app">
    <router-view />
  </div>
</template>

<script setup>
import { useUserStore } from './stores/user'

const { init } = useUserStore()
init()
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f7fa;
  color: #333;
}

.app {
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.btn {
  display: inline-block;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #409eff;
  color: white;
}

.btn-primary:hover {
  background-color: #66b1ff;
}

.btn-success {
  background-color: #67c23a;
  color: white;
}

.btn-success:hover {
  background-color: #85ce61;
}

.btn-warning {
  background-color: #e6a23c;
  color: white;
}

.btn-warning:hover {
  background-color: #ebb563;
}

.btn-danger {
  background-color: #f56c6c;
  color: white;
}

.btn-danger:hover {
  background-color: #f78989;
}

.btn-outline {
  background-color: transparent;
  border: 1px solid #dcdfe6;
  color: #666;
}

.btn-outline:hover {
  background-color: #f5f7fa;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ebeef5;
}

.table th {
  background-color: #f5f7fa;
  font-weight: 600;
}

.table tr:hover {
  background-color: #fafafa;
}

.status-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-applied {
  background-color: #ecf5ff;
  color: #409eff;
}

.status-pending {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.status-interview {
  background-color: #f0f9eb;
  color: #67c23a;
}

.status-rejected {
  background-color: #fef0f0;
  color: #f56c6c;
}

.status-active {
  background-color: #f0f9eb;
  color: #67c23a;
}

.status-inactive {
  background-color: #f5f5f5;
  color: #909399;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 20px;
}

.pagination button {
  padding: 6px 12px;
  border: 1px solid #dcdfe6;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.pagination button.active {
  background-color: #409eff;
  color: white;
  border-color: #409eff;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  padding: 24px;
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-header h3 {
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 24px;
  border-radius: 4px;
  color: white;
  z-index: 2000;
  animation: slideIn 0.3s ease;
}

.toast-success {
  background-color: #67c23a;
}

.toast-error {
  background-color: #f56c6c;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0 8px;
  height: 20px;
  font-size: 12px;
  font-weight: 500;
  border-radius: 10px;
  background-color: #f5f7fa;
  color: #666;
}

.badge-primary {
  background-color: #ecf5ff;
  color: #409eff;
}

.badge-success {
  background-color: #f0f9eb;
  color: #67c23a;
}

.badge-warning {
  background-color: #fdf6ec;
  color: #e6a23c;
}

.badge-danger {
  background-color: #fef0f0;
  color: #f56c6c;
}
</style>