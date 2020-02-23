import { Component, OnInit } from '@angular/core';
import { ActionSheetController } from '@ionic/angular';
import { ToastController } from '@ionic/angular';
import { MainControllerService } from '../services/main-controller.service';
import { ModalController } from '@ionic/angular';
@Component({
  selector: 'app-tab3',
  templateUrl: './tab3.page.html',
  styleUrls: ['./tab3.page.scss'],
})
export class Tab3Page implements OnInit {

  myCartList: any;
  cartCount: number;
  prodList: any;

  constructor(
    private mainController: MainControllerService,
  ) {
    this.myCartList = [];
    this.prodList = [];
  }


  private getProducts() {
    this.mainController.getProductList().toPromise().then(r => {
      this.prodList = JSON.parse(r);
      this.prodList.reverse();
      this.prodList.map(v => {
        v.ProductPrice = 'Buko';
      });
    });
  }

  ngOnInit() {
    this.getProducts();
  }

}
