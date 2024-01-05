var app=new Vue({
    el:'#app',

    data:{
        // 时间
        timer:null,
        //测试循环
        rtimer:null,

        faultCss:"fault-content",
        indicatorText:"indicator-text",
        // new
        newShow:false,
        varNumber:"",
        interval:"",
        // label
        startdrag:false,
        labelShow:false,
        //流程图选择
        options: [{
            value: 1,
            label: 'TE过程流程图'
          }, {
            value: 2,
            label: '合成氨过程'
          }, {
            value: 3,
            label: 'FCC（流化催化裂化）过程流程图（1）'
          }, {
            value: 4,
            label: 'FCC（流化催化裂化）过程流程图（2）'
          }, {
            value: 5,
            label: '其他'
          }],
          value: '',

        // 测点标注
        labelData: [
            // {
            //     data:1
            // }
        ],
         // 小框框数据
        faultData:[
            
        ],

        //describe
        describeShow:false,
        describeDatas: [
            // {
            //     dID:""
                // content:""
            // }
        ],
        // 故障内容
        faultContent:"",
        // 流程图url
        flowChartUrl:"",
        
       
        faultDataIndex:0,
        // 文档
        fileName1:"",
        fileName2:"",
        flowChart:"",
        //文档内容
        fileContent1:"",
        fileContent2:"",


        arithmetic:[
            "Random Forest", 
            "PCA", 
            "SVM", 
            "BPN",
            "BP",
            "CNN",
            "GMM",
            "LDA",
            "RBF"
        ],

        arithmeticSelect:"",

        indicator:[
            {
                image:"images/指示灯1.png",
                text:"无结果"
            },
            {
                image:"images/指示灯2.png",
                text:"无故障"
            },
            {
                image:"images/指示灯3.png",
                text:"出现故障" 
            }
            
        ],
        // 指示语
        indicatortext:"",
        // 指示号
        indicatorindex: 0,
        //对象名称
        objectName:"",
        //时间
        datatimes:0,
        
       
        // 是否测试
        isTest:false,
        state:null,
        

    },

    methods:{
        judge(){

            
                if(!(/^[a-zA-Z]:(((\\(?! )[^/:*?<>\""|\\]+)+\\?)|(\\)?)\s*$/.test(this.fileContent1))){
                    alert("训练样本文件地址格式错误！")
                    
                }
           
                if(!(/^[a-zA-Z]:(((\\(?! )[^/:*?<>\""|\\]+)+\\?)|(\\)?)\s*$/.test(this.fileContent2))){
                    alert("测试样本文件地址格式错误！")
                    
                }

                if((/^[a-zA-Z]:(((\\(?! )[^/:*?<>\""|\\]+)+\\?)|(\\)?)\s*$/.test(this.fileContent1))&&(/^[a-zA-Z]:(((\\(?! )[^/:*?<>\""|\\]+)+\\?)|(\\)?)\s*$/.test(this.fileContent2))){
                    this.newShow=false
                }
                else{
                    switch (this.value){
                        case 1:
                            this.flowChartUrl = "images/故障图/1.png"  
                            break;
                        case 2:
                            this.flowChartUrl = "images/故障图/2.png"  
                            break;
                        case 3:
                            this.flowChartUrl = "images/故障图/3.jpg"  
                            break;
                        case 4:
                            this.flowChartUrl = "images/故障图/4.jpg" 
                            break;
                        case 5:
                            this.runHandleAvatarSuccess()
                            break;
                    }
                }
    
        },


        //清除新建内容
        Cancel(){
            this.objectName="";
            this.newShow=false;
            this.fileContent1="";
            this.fileContent2="";
            this.varNumber="";
            this.interval="";
        },
        
        labelNew(){
            this.labelData.push({
                lID:"",
            })
        },
       
        labelDelete(index, row) {
          this.labelData.splice (index,1)
          this.faultData.splice(index,1)
        },

        //清除所有小框及其数据
        ClearlabelShow(){
            this.labelData=[]
            this.faultData=[]
            this.labelShow=false
        },

        //新建一条用户自己编写的描述数据
        describeNew(){
            this.describeDatas.push({
                dID:"",
                content:""
            })
        },

            //删除一条用户自己编写的描述数据
        describeDelete(index, row) {
            this.describeDatas.splice (index,1)

          },

          //清除用户自己编写的描述数据
        ClearDescrible(){
            this.describeDatas=[]
            this.describeShow=false
        },

       //抓取显示数据小框框的位置
        graspPosition(index,e){   
            this.labelShow=false    
            this.startdrag=true
            if(this.faultData[index]==null){
                this.faultData.push(
                    {
                        mdata:"",
                        top:e.clientY+"px",
                        left:e.clientX+"px",
                    }
                )
            }else{
                this.faultData[index].top=e.clientY-233+"px",
                this.faultData[index].left=e.clientX-50+"px"
            }
            faultDataIndex=index
        },
        move(e){
            if(this.startdrag){
                this.faultData[faultDataIndex].top=e.clientY-233+"px",
                this.faultData[faultDataIndex].left=e.clientX-50+"px"
            }
        },

        //智能匹配
        /*matching(){
            this.state = 3,
            arithmetics=[
                "Random Forest", 
                "PCA", 
                "SVM", 
                "BPN",
                "BP",
                "CNN",
                "GMM",
                "LDA",
                "RBF"
            ],
            axios.post("http://127.0.0.1:5000/ainfo",{
                state:this.state, //用于后端判断是训练还是测试 1为训练 2为测试
                fileContent1:this.fileContent1,//训练数据文件地址
                fileContent2:this.fileContent2,//测试数据文件地址
                //arithmetic:this.arithmeticSelect,//算法
                varNumber:this.varNumber,//训练样本数       
            },)
            .then(function(response){
                //console.log(this.arithmetic);
                if(response.data.recommend>0){
                    this.arithmeticSelect=arithmetics[parseInt(response.data.recommend)];
                    console.log(arithmetics[parseInt(response.data.recommend)]);
                }
                
            },function(err){})
        },*/
        matching(){
            this.state = 3
            that=this
            axios.post("http://127.0.0.1:5000/ainfo",{
                state:that.state, //用于后端判断是训练还是测试 1为训练 2为测试
                fileContent1:that.fileContent1,//训练数据文件地址
                fileContent2:that.fileContent2,//测试数据文件地址
                // arithmetic:this.arithmeticSelect,//算法
                varNumber:that.varNumber,//训练样本数       
            },)
            .then(function(response){
                
                if(response.data.recommend>=0){
                    that.arithmeticSelect=that.arithmetic[response.data.recommend]
                }
                
            },function(err){})
        },

        // 搜索功能
        Search(){
            window.location.href="https://www.hhmnb.top/搜索.docx"

        },
        //帮助功能
        help(){
            window.location.href="https://www.hhmnb.top/帮助文档.docx"

        },

        // 指示灯图片获取
        getImage:function(){
            this.indicatortext=this.indicator[this.indicatorindex].text
            return this.indicator[this.indicatorindex].image
        },

        //***************  图片文件获取
        runHandleAvatarSuccess(){

            document.getElementsByTagName("input")[4].click()

        },

        handleAvatarSuccess(res, file) {
            console.log(res.raw);
            this.flowChartUrl = URL.createObjectURL(res.raw);

          },


        //********* 清空
        clear(){
        clearInterval(this.timer)
        this.timer=null
        clearInterval(this.rtimer)
        this.rtimer=null

        this.datatimes=0
                // new
        this.newShow=false,
        this.varNumber="",
        this.interval="",
        // label
        this.startdrag=false,
        this.labelShow=false,
        // 测点标注
        this.labelData=[]
         // 小框框数据
         this.faultData=[]

        //describe
        this.describeShow=false,
        this.describeDatas=[]
        // 流程图url
        this.flowChartUrl="",
        this.value='',
       
        this.faultDataIndex=0,


        this.fileName1="",
        this.fileName2="",

        this.objectName="",

        this.indicatorindex= 0

        this.arithmeticSelect=""
        //文档内容
        this.fileContent1=""
        this.fileContent2=""
        // 故障内容
        this.faultContent=""
       
       // 是否测试
       this.isTest=true //用于前端判断是训练还是测试
        this.state=1 //用于后端判断是训练还是测试 1为训练 2为测试
      
        },

        isDrill(){
            if(this.fileContent1==""){
                alert("请在“新建”中完成项目创建，并正确键入样本文件地址！")
            }else if(this.arithmeticSelect==""){
                alert("请选择算法")
            }else if(this.varNumber==""){
                alert("请在“新建”中完成项目创建，并键入正确的样本文件数！")
            }else{
                this.Drill()
            }
        },
        
        //*****************训练上传文档内容
        Drill(){
            //console.log("length"+this.labelData.length)
            this.isTest=false,
            this.state=1;
            that = this;
            const loading = this.$loading({
                lock: true,
                text: '正在训练',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
              });
            
              
            console.log("run");
            axios.post("http://127.0.0.1:5000/ainfo",{
                state:that.state, //用于后端判断是训练还是测试 1为训练 2为测试
                fileContent1:that.fileContent1,//训练数据文件地址
                fileContent2:that.fileContent2,//测试数据文件地址
                arithmetic:that.arithmeticSelect,//算法
                varNumber:that.varNumber,//训练样本数
                
            },)
            .then(function(response){
                loading.close();
                 
                 if(response.data.tr==1){//但前端每次执行都会刷新初始值，因此该判断失效
                    that.isTest=true
                    that.state=2
                    alert("训练完毕！")
                 }

            },function(err){})    
            
        },

        //测试
        Testo(){
            //console.log("length"+this.labelData.length)
            console.log(this.isTest);
            if(true){//每次运行时，isTest都会恢复初始值，不知如何解决
                var rinterval=this.interval*1000
                
                var num=1;
                this.state=2;

                var that = this;
                this.rtimer = window.setInterval(() => {
                    num++;
                    //console.log(num);
                    axios.post("http://127.0.0.1:5000/ainfo",{
                            state:that.state, //用于后端判断是训练还是测试 1为训练 2为测试
                            fileContent1:that.fileContent1,//训练数据文件地址
                            fileContent2:that.fileContent2,//测试数据文件地址
                            arithmetic:that.arithmeticSelect,//算法
                            varNumber:that.varNumber,//训练样本数
                            num:num//测试第几排
                        },)
                        .then(function(response){

                            console.log(response); 
                            that.indicatorindex=1
                            
                            if(that.labelData!=null){
                                //console.log("length"+this.labelData.length)
                            for(var i=0;i<that.labelData.length;i++){
                                console.log(that.labelData[i].lID); 
                                //if(parseInt(that.labelData[i].lID)==i){
                                    that.faultData[i].mdata=response.data.data[parseInt(that.labelData[i].lID)]
                                //}
                             };
                            }

                            console.log(that.faultData)
                            if(response.data.judge[0]!=0&&response.data.judge[0]!=null){
                                that.indicatorindex=2
                                that.describeDatas.forEach(item => {
                                    if(item.dID==response.data.judge[0]){
                                        that.faultContent = item.content
                                        clearInterval(that.rtimer)
                                        that.rtimer=null
                                        clearInterval(that.timer)
                                        that.timer=null
                                    }
                                });
                                // faultContent=this.describeDatas[][response.data.judge[0]]//返回的错误编号，使之对应显示在前端界面上
                            }
                            

                    },function(err){})
                    if(that.isTest){
                        clearInterval(that.rtimer)
                        that.rtimer=null
                    }
                }, rinterval);

                clearTimeout(this.timer)
                this.datatimes=0
                this.timer = window.setInterval(() => {
                    this.datatimes++;
                }, 1000);
            }
        }

    },
    
})

function judgeColor (indicatorindex) {
    console.log(app);
    console.log(app._data)
    if(indicatorindex== 2){
        app._data.faultCss="fault-content changered",
        app._data.indicatorText="indicator-text changered"
    }else{
        app._data.faultCss="fault-content",
        app._data.indicatorText="indicator-text"
    }
    console.log("好了")
}
