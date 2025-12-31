"""
🛡️ 工业级浏览器指纹防御系统
多维度抹除浏览器指纹，对抗高级反爬虫检测

防御层级：
1. WebGL 指纹扰动（供应商、渲染器信息伪装）
2. Canvas 指纹随机化（像素级噪点注入）
3. Audio 指纹混淆（音频上下文特征变化）
4. 字体指纹保护（字体列表随机化）
5. 硬件指纹变换（CPU核心数、内存大小）
6. 时区和语言动态化
7. 屏幕分辨率真实化

作者：iostoupin Team
日期：2025-12-31
"""

import random
from typing import Dict, List, Optional
from playwright.async_api import BrowserContext, Page


class FingerprintDefense:
    """浏览器指纹防御核心类"""
    
    # WebGL 供应商池（真实GPU供应商）
    WEBGL_VENDORS = [
        {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA GeForce RTX 4090 Direct3D11 vs_5_0 ps_5_0)"},
        {"vendor": "Google Inc. (AMD)", "renderer": "ANGLE (AMD Radeon RX 7900 XTX Direct3D11 vs_5_0 ps_5_0)"},
        {"vendor": "Google Inc. (Intel)", "renderer": "ANGLE (Intel(R) UHD Graphics 770 Direct3D11 vs_5_0 ps_5_0)"},
        {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA GeForce RTX 3080 Direct3D11 vs_5_0 ps_5_0)"},
        {"vendor": "Google Inc. (AMD)", "renderer": "ANGLE (AMD Radeon RX 6800 XT Direct3D11 vs_5_0 ps_5_0)"},
    ]
    
    # Canvas 噪点强度范围
    CANVAS_NOISE_MIN = 0.0001
    CANVAS_NOISE_MAX = 0.001
    
    # 真实屏幕分辨率池
    SCREEN_RESOLUTIONS = [
        {"width": 1920, "height": 1080, "colorDepth": 24, "pixelRatio": 1.0},
        {"width": 2560, "height": 1440, "colorDepth": 24, "pixelRatio": 1.0},
        {"width": 3840, "height": 2160, "colorDepth": 24, "pixelRatio": 1.0},  # 4K
        {"width": 1366, "height": 768, "colorDepth": 24, "pixelRatio": 1.0},
        {"width": 1440, "height": 900, "colorDepth": 24, "pixelRatio": 1.0},
    ]
    
    # CPU 核心数池（真实分布）
    CPU_CORES = [4, 6, 8, 12, 16, 24]
    
    # 内存大小池（GB，真实分布）
    MEMORY_SIZES = [8, 16, 32, 64]
    
    def __init__(self):
        """初始化指纹防御"""
        self.webgl_config = random.choice(self.WEBGL_VENDORS)
        self.canvas_noise = random.uniform(self.CANVAS_NOISE_MIN, self.CANVAS_NOISE_MAX)
        self.screen_config = random.choice(self.SCREEN_RESOLUTIONS)
        self.cpu_cores = random.choice(self.CPU_CORES)
        self.memory_size = random.choice(self.MEMORY_SIZES)
        
        print(f"🛡️ 指纹配置: GPU={self.webgl_config['vendor'][:30]}, "
              f"分辨率={self.screen_config['width']}x{self.screen_config['height']}, "
              f"CPU={self.cpu_cores}核")
    
    def get_defense_script(self) -> str:
        """
        生成完整的指纹防御 JavaScript 脚本
        
        Returns:
            完整的防御脚本字符串
        """
        return f"""
// ========================================
// 🛡️ 工业级浏览器指纹防御系统
// ========================================

(function() {{
    'use strict';
    
    const config = {{
        webgl: {{
            vendor: "{self.webgl_config['vendor']}",
            renderer: "{self.webgl_config['renderer']}"
        }},
        canvas: {{
            noise: {self.canvas_noise}
        }},
        screen: {{
            width: {self.screen_config['width']},
            height: {self.screen_config['height']},
            colorDepth: {self.screen_config['colorDepth']},
            pixelRatio: {self.screen_config['pixelRatio']}
        }},
        hardware: {{
            cpuCores: {self.cpu_cores},
            memoryGB: {self.memory_size}
        }}
    }};
    
    // ========================================
    // 1. WebGL 指纹防御
    // ========================================
    const getParameterProxyHandler = {{
        apply: function(target, thisArg, args) {{
            const param = args[0];
            
            // 拦截 VENDOR 和 RENDERER 查询
            if (param === 37445) {{  // UNMASKED_VENDOR_WEBGL
                return config.webgl.vendor;
            }}
            if (param === 37446) {{  // UNMASKED_RENDERER_WEBGL
                return config.webgl.renderer;
            }}
            
            return target.apply(thisArg, args);
        }}
    }};
    
    // 覆盖 WebGLRenderingContext
    const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = new Proxy(
        originalGetParameter,
        getParameterProxyHandler
    );
    
    // 覆盖 WebGL2RenderingContext
    if (window.WebGL2RenderingContext) {{
        const originalGetParameter2 = WebGL2RenderingContext.prototype.getParameter;
        WebGL2RenderingContext.prototype.getParameter = new Proxy(
            originalGetParameter2,
            getParameterProxyHandler
        );
    }}
    
    // ========================================
    // 2. Canvas 指纹防御（噪点注入）
    // ========================================
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    const originalToBlob = HTMLCanvasElement.prototype.toBlob;
    const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
    
    // 注入噪点函数
    function injectCanvasNoise(imageData) {{
        const data = imageData.data;
        for (let i = 0; i < data.length; i += 4) {{
            // 对每个像素的 RGB 通道注入微小噪点
            const noise = Math.floor(Math.random() * config.canvas.noise * 255);
            data[i] = Math.min(255, data[i] + noise);      // R
            data[i+1] = Math.min(255, data[i+1] + noise);  // G
            data[i+2] = Math.min(255, data[i+2] + noise);  // B
            // Alpha 通道不变
        }}
        return imageData;
    }}
    
    // 覆盖 toDataURL
    HTMLCanvasElement.prototype.toDataURL = function() {{
        const context = this.getContext('2d');
        if (context) {{
            const imageData = context.getImageData(0, 0, this.width, this.height);
            injectCanvasNoise(imageData);
            context.putImageData(imageData, 0, 0);
        }}
        return originalToDataURL.apply(this, arguments);
    }};
    
    // 覆盖 getImageData
    CanvasRenderingContext2D.prototype.getImageData = function() {{
        const imageData = originalGetImageData.apply(this, arguments);
        return injectCanvasNoise(imageData);
    }};
    
    // ========================================
    // 3. Audio 指纹防御
    // ========================================
    const originalCreateAnalyser = AudioContext.prototype.createAnalyser;
    AudioContext.prototype.createAnalyser = function() {{
        const analyser = originalCreateAnalyser.apply(this, arguments);
        
        // 覆盖频率数据获取方法
        const originalGetFloatFrequencyData = analyser.getFloatFrequencyData;
        analyser.getFloatFrequencyData = function(array) {{
            originalGetFloatFrequencyData.apply(this, arguments);
            // 注入微小噪声
            for (let i = 0; i < array.length; i++) {{
                array[i] += Math.random() * 0.001;
            }}
        }};
        
        return analyser;
    }};
    
    // ========================================
    // 4. 字体指纹防御
    // ========================================
    const originalFonts = Object.getOwnPropertyDescriptor(Document.prototype, 'fonts');
    Object.defineProperty(Document.prototype, 'fonts', {{
        get: function() {{
            const fonts = originalFonts.get.call(this);
            
            // 随机化字体检测结果
            const originalCheck = fonts.check;
            fonts.check = function() {{
                // 随机返回部分字体可用
                return Math.random() > 0.3 ? originalCheck.apply(this, arguments) : false;
            }};
            
            return fonts;
        }}
    }});
    
    // ========================================
    // 5. 硬件指纹防御
    // ========================================
    Object.defineProperty(navigator, 'hardwareConcurrency', {{
        get: () => config.hardware.cpuCores
    }});
    
    Object.defineProperty(navigator, 'deviceMemory', {{
        get: () => config.hardware.memoryGB
    }});
    
    // ========================================
    // 6. 屏幕指纹防御
    // ========================================
    Object.defineProperty(screen, 'width', {{
        get: () => config.screen.width
    }});
    
    Object.defineProperty(screen, 'height', {{
        get: () => config.screen.height
    }});
    
    Object.defineProperty(screen, 'availWidth', {{
        get: () => config.screen.width
    }});
    
    Object.defineProperty(screen, 'availHeight', {{
        get: () => config.screen.height - 40  // 减去任务栏高度
    }});
    
    Object.defineProperty(screen, 'colorDepth', {{
        get: () => config.screen.colorDepth
    }});
    
    Object.defineProperty(window, 'devicePixelRatio', {{
        get: () => config.screen.pixelRatio
    }});
    
    // ========================================
    // 7. WebDriver 检测防御（增强版）
    // ========================================
    Object.defineProperty(navigator, 'webdriver', {{
        get: () => false
    }});
    
    // 删除 __webdriver_* 属性
    delete navigator.__proto__.webdriver;
    
    // ========================================
    // 8. Chrome Runtime 伪装
    // ========================================
    window.chrome = {{
        runtime: {{
            connect: function() {{ return null; }},
            sendMessage: function() {{ return null; }}
        }},
        loadTimes: function() {{ 
            return {{
                requestTime: Date.now() / 1000 - Math.random() * 10,
                startLoadTime: Date.now() / 1000 - Math.random() * 5,
                commitLoadTime: Date.now() / 1000 - Math.random() * 2,
                finishDocumentLoadTime: Date.now() / 1000,
                finishLoadTime: Date.now() / 1000 + Math.random() * 0.5,
                firstPaintTime: Date.now() / 1000 - Math.random() * 1,
                firstPaintAfterLoadTime: 0,
                navigationType: "Other",
                wasFetchedViaSpdy: false,
                wasNpnNegotiated: true,
                npnNegotiatedProtocol: "h2",
                wasAlternateProtocolAvailable: false,
                connectionInfo: "h2"
            }};
        }},
        csi: function() {{
            return {{
                startE: Date.now() - Math.random() * 1000,
                onloadT: Date.now() + Math.random() * 500,
                pageT: Math.random() * 2000 + 1000,
                tran: 15
            }};
        }},
        app: {{}}
    }};
    
    // ========================================
    // 9. Permissions API 修复
    // ========================================
    const originalPermissionQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => {{
        if (parameters.name === 'notifications') {{
            return Promise.resolve({{ state: Notification.permission }});
        }}
        return originalPermissionQuery(parameters);
    }};
    
    // ========================================
    // 10. Plugin 伪装
    // ========================================
    Object.defineProperty(navigator, 'plugins', {{
        get: () => [
            {{
                name: 'Chrome PDF Plugin',
                filename: 'internal-pdf-viewer',
                description: 'Portable Document Format'
            }},
            {{
                name: 'Chrome PDF Viewer',
                filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
                description: ''
            }},
            {{
                name: 'Native Client',
                filename: 'internal-nacl-plugin',
                description: ''
            }}
        ]
    }});
    
    // ========================================
    // 11. 语言和时区
    // ========================================
    Object.defineProperty(navigator, 'languages', {{
        get: () => ['zh-CN', 'zh', 'en-US', 'en']
    }});
    
    Object.defineProperty(navigator, 'language', {{
        get: () => 'zh-CN'
    }});
    
    // ========================================
    // 完成标记
    // ========================================
    console.log('🛡️ 工业级指纹防御已激活');
    console.log('  • WebGL: ✓ 供应商已伪装');
    console.log('  • Canvas: ✓ 噪点已注入');
    console.log('  • Audio: ✓ 频率已扰动');
    console.log('  • 字体: ✓ 检测已混淆');
    console.log('  • 硬件: ✓ 参数已变换');
    console.log('  • 屏幕: ✓ 分辨率已设置');
    console.log('  • WebDriver: ✓ 特征已清除');
    console.log('  • Chrome: ✓ Runtime已伪装');
    
}})();
"""
    
    async def apply_to_context(self, context: BrowserContext) -> None:
        """
        将指纹防御应用到浏览器上下文
        
        Args:
            context: Playwright BrowserContext
        """
        try:
            script = self.get_defense_script()
            await context.add_init_script(script)
            print("✅ 工业级指纹防御已注入到浏览器上下文")
        except Exception as e:
            print(f"⚠️ 指纹防御注入部分失败: {e}")
    
    async def apply_to_page(self, page: Page) -> None:
        """
        将指纹防御应用到单个页面
        
        Args:
            page: Playwright Page
        """
        try:
            script = self.get_defense_script()
            await page.add_init_script(script)
            print("✅ 工业级指纹防御已注入到页面")
        except Exception as e:
            print(f"⚠️ 指纹防御注入部分失败: {e}")
    
    def get_config_summary(self) -> Dict:
        """
        获取当前指纹配置摘要
        
        Returns:
            配置字典
        """
        return {
            "webgl_vendor": self.webgl_config["vendor"],
            "webgl_renderer": self.webgl_config["renderer"],
            "canvas_noise": self.canvas_noise,
            "screen_resolution": f"{self.screen_config['width']}x{self.screen_config['height']}",
            "cpu_cores": self.cpu_cores,
            "memory_gb": self.memory_size
        }


# ========================================
# 便捷函数
# ========================================

async def apply_fingerprint_defense(context: BrowserContext) -> FingerprintDefense:
    """
    快速应用指纹防御到浏览器上下文
    
    Args:
        context: Playwright BrowserContext
    
    Returns:
        FingerprintDefense 实例
    
    示例:
        defense = await apply_fingerprint_defense(context)
        print(defense.get_config_summary())
    """
    defense = FingerprintDefense()
    await defense.apply_to_context(context)
    return defense


if __name__ == "__main__":
    # 测试脚本生成
    defense = FingerprintDefense()
    print("\n" + "="*60)
    print("🛡️ 指纹防御配置")
    print("="*60)
    for key, value in defense.get_config_summary().items():
        print(f"  {key}: {value}")
    print("="*60)
    print(f"\n📜 脚本长度: {len(defense.get_defense_script())} 字符")
    print("✅ 指纹防御模块已就绪")
