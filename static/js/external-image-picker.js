/**
 * External Image Picker for TinyMCE
 * Cho phép chọn hình ảnh từ URL bên ngoài thay vì upload
 */

class ExternalImagePicker {
    constructor(callback) {
        this.callback = callback;
        this.supportedServices = {};
        this.init();
    }

    async init() {
        // Lấy danh sách dịch vụ được hỗ trợ
        try {
            const response = await fetch('/admin/get-supported-services');
            this.supportedServices = await response.json();
        } catch (error) {
            console.error('Failed to load supported services:', error);
        }
        
        this.createModal();
    }

    createModal() {
        // Tạo modal HTML
        const modalHTML = `
            <div id="external-image-modal" class="fixed inset-0 bg-black bg-opacity-50 z-50 hidden">
                <div class="flex items-center justify-center min-h-screen p-4">
                    <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-screen overflow-y-auto">
                        <div class="p-6">
                            <div class="flex justify-between items-center mb-6">
                                <h3 class="text-xl font-bold text-gray-800">
                                    <i class="fas fa-link mr-2 text-blue-500"></i>
                                    Chèn hình ảnh từ URL
                                </h3>
                                <button id="close-modal" class="text-gray-400 hover:text-gray-600">
                                    <i class="fas fa-times text-xl"></i>
                                </button>
                            </div>

                            <!-- URL Input -->
                            <div class="mb-6">
                                <label class="block text-sm font-medium text-gray-700 mb-2">
                                    URL hình ảnh <span class="text-red-500">*</span>
                                </label>
                                <input type="url" id="image-url-input" 
                                       class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                                       placeholder="https://example.com/image.jpg">
                                <div id="url-error" class="text-red-500 text-sm mt-1 hidden"></div>
                            </div>

                            <!-- Preview -->
                            <div id="image-preview" class="mb-6 hidden">
                                <label class="block text-sm font-medium text-gray-700 mb-2">Xem trước:</label>
                                <div class="border border-gray-200 rounded-lg p-4 bg-gray-50">
                                    <img id="preview-image" src="" alt="Preview" 
                                         class="max-w-full max-h-64 mx-auto rounded shadow">
                                </div>
                            </div>

                            <!-- Supported Services -->
                            <div class="mb-6">
                                <h4 class="text-lg font-semibold text-gray-800 mb-4">
                                    <i class="fas fa-cloud mr-2 text-green-500"></i>
                                    Dịch vụ được hỗ trợ
                                </h4>
                                <div id="supported-services" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <!-- Services will be populated here -->
                                </div>
                            </div>

                            <!-- Instructions -->
                            <div class="mb-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
                                <h4 class="font-medium text-blue-800 mb-2">
                                    <i class="fas fa-info-circle mr-2"></i>
                                    Hướng dẫn sử dụng
                                </h4>
                                <ul class="text-sm text-blue-700 space-y-1">
                                    <li>• Dán URL hình ảnh vào ô trên</li>
                                    <li>• Hệ thống sẽ tự động xử lý URL từ Google Drive, OneDrive, Dropbox</li>
                                    <li>• Kiểm tra xem trước trước khi chèn</li>
                                    <li>• URL phải trỏ trực tiếp đến file hình ảnh</li>
                                </ul>
                            </div>

                            <!-- Actions -->
                            <div class="flex justify-end space-x-3">
                                <button id="cancel-btn" 
                                        class="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50">
                                    Hủy
                                </button>
                                <button id="insert-btn" 
                                        class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed" 
                                        disabled>
                                    <i class="fas fa-check mr-2"></i>
                                    Chèn hình ảnh
                                </button>
                            </div>

                            <!-- Loading -->
                            <div id="loading" class="hidden text-center py-4">
                                <i class="fas fa-spinner fa-spin text-blue-500 text-xl"></i>
                                <p class="text-gray-600 mt-2">Đang xử lý URL...</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Thêm modal vào DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Populate supported services
        this.populateSupportedServices();
        
        // Bind events
        this.bindEvents();
    }

    populateSupportedServices() {
        const container = document.getElementById('supported-services');
        
        Object.entries(this.supportedServices).forEach(([key, service]) => {
            const serviceHTML = `
                <div class="border border-gray-200 rounded-lg p-3 hover:bg-gray-50">
                    <h5 class="font-medium text-gray-800 mb-1">${service.name}</h5>
                    <p class="text-xs text-gray-600 mb-2">${service.instructions}</p>
                    <code class="text-xs bg-gray-100 px-2 py-1 rounded text-gray-700 block truncate">
                        ${service.example}
                    </code>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', serviceHTML);
        });
    }

    bindEvents() {
        const modal = document.getElementById('external-image-modal');
        const urlInput = document.getElementById('image-url-input');
        const insertBtn = document.getElementById('insert-btn');
        const cancelBtn = document.getElementById('cancel-btn');
        const closeBtn = document.getElementById('close-modal');

        // Close modal
        [cancelBtn, closeBtn].forEach(btn => {
            btn.addEventListener('click', () => this.hideModal());
        });

        // Close on backdrop click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) this.hideModal();
        });

        // URL input change
        urlInput.addEventListener('input', this.debounce(() => {
            this.validateAndPreviewURL();
        }, 500));

        // Insert button
        insertBtn.addEventListener('click', () => {
            this.insertImage();
        });

        // ESC key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
                this.hideModal();
            }
        });
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    async validateAndPreviewURL() {
        const urlInput = document.getElementById('image-url-input');
        const errorDiv = document.getElementById('url-error');
        const previewDiv = document.getElementById('image-preview');
        const previewImg = document.getElementById('preview-image');
        const insertBtn = document.getElementById('insert-btn');
        const loading = document.getElementById('loading');

        const url = urlInput.value.trim();
        
        // Reset states
        errorDiv.classList.add('hidden');
        previewDiv.classList.add('hidden');
        insertBtn.disabled = true;

        if (!url) return;

        // Show loading
        loading.classList.remove('hidden');

        try {
            // Gửi URL đến server để xử lý
            const response = await fetch('/admin/process-external-image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });

            const result = await response.json();

            if (response.ok) {
                // URL hợp lệ - hiển thị preview
                previewImg.src = result.location;
                previewImg.onload = () => {
                    previewDiv.classList.remove('hidden');
                    insertBtn.disabled = false;
                    this.processedUrl = result.location;
                };
                previewImg.onerror = () => {
                    this.showError('Không thể tải hình ảnh từ URL này');
                };
            } else {
                this.showError(result.error || 'URL không hợp lệ');
            }
        } catch (error) {
            this.showError('Lỗi khi xử lý URL: ' + error.message);
        } finally {
            loading.classList.add('hidden');
        }
    }

    showError(message) {
        const errorDiv = document.getElementById('url-error');
        errorDiv.textContent = message;
        errorDiv.classList.remove('hidden');
    }

    insertImage() {
        if (this.processedUrl && this.callback) {
            const urlInput = document.getElementById('image-url-input');
            const filename = urlInput.value.split('/').pop() || 'external-image';
            
            this.callback(this.processedUrl, {
                alt: filename,
                title: filename
            });
            
            this.hideModal();
        }
    }

    showModal() {
        const modal = document.getElementById('external-image-modal');
        modal.classList.remove('hidden');
        document.getElementById('image-url-input').focus();
    }

    hideModal() {
        const modal = document.getElementById('external-image-modal');
        modal.classList.add('hidden');
        
        // Reset form
        document.getElementById('image-url-input').value = '';
        document.getElementById('url-error').classList.add('hidden');
        document.getElementById('image-preview').classList.add('hidden');
        document.getElementById('insert-btn').disabled = true;
        this.processedUrl = null;
    }
}

// Export for use in TinyMCE configuration
window.ExternalImagePicker = ExternalImagePicker;

